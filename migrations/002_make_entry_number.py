"""Peewee migrations -- 002_make_entry_number.py."""

from contextlib import suppress
import peewee as pw
from peewee_migrate import Migrator

with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    migrator.add_fields(
        'income_outcome',
        voucher_year=pw.IntegerField(null=True),
        voucher_no=pw.IntegerField(null=True),
    )

    @migrator.create_model
    class VoucherCounter(pw.Model):
        id = pw.AutoField()
        type = pw.CharField(max_length=255)
        year = pw.IntegerField()
        last_no = pw.IntegerField(default=0)

        class Meta:
            table_name = "voucher_counter"
            indexes = [(('type', 'year'), True)]
            
    def _backfill_numbers(migrator: Migrator, db: pw.Database):
        IncomeOutcome = migrator.orm['income_outcome']
        VoucherCounter = migrator.orm['voucher_counter']

        with db.atomic():
            cls_name = db.__class__.__name__.lower()
            if 'postgre' in cls_name:
                db.execute_sql("""
                    UPDATE income_outcome
                    SET voucher_year = EXTRACT(YEAR FROM date)::int
                    WHERE voucher_year IS NULL;
                """)
            else:
                # SQLite
                db.execute_sql("""
                    UPDATE income_outcome
                    SET voucher_year = CAST(STRFTIME('%Y', date) AS INTEGER)
                    WHERE voucher_year IS NULL;
                """)

        counters = {}  # {(type, year): last_no}
        with db.atomic():
            q = (IncomeOutcome
                 .select(IncomeOutcome.id,
                         IncomeOutcome.type,
                         IncomeOutcome.voucher_year,
                         IncomeOutcome.date,
                         IncomeOutcome.created_at)
                 .order_by(IncomeOutcome.type,
                           IncomeOutcome.voucher_year,
                           IncomeOutcome.date,
                           IncomeOutcome.created_at,
                           IncomeOutcome.id))

            current_key = None
            running = 0
            for rec in q:
                key = (rec.type, rec.voucher_year)
                if key != current_key:
                    current_key = key
                    running = 0
                running += 1
                (IncomeOutcome
                 .update(voucher_no=running)
                 .where(IncomeOutcome.id == rec.id)
                 .execute())
                counters[key] = running

        with db.atomic():
            for (typ, yr), last_no in counters.items():
                try:
                    VoucherCounter.create(type=typ, year=yr, last_no=last_no)
                except Exception:
                    (VoucherCounter
                     .update(last_no=last_no)
                     .where((VoucherCounter.type == typ) & (VoucherCounter.year == yr))
                     .execute())

        with suppress(Exception):
            migrator.add_not_null('income_outcome', 'voucher_year')

        with suppress(Exception):
            migrator.add_not_null('income_outcome', 'voucher_no')


    migrator.run(_backfill_numbers, migrator, database)


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    migrator.remove_fields('income_outcome', 'voucher_year', 'voucher_no')
    migrator.remove_model('voucher_counter')
