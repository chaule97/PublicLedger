# controllers/finance_controller.py
import datetime
from db import database
from models import IncomeOutcome, VoucherCounter


class FinanceController:

    @staticmethod
    def add_entry(data):
        """
        data = {
            'type': 'income' | 'outcome',
            'name': str,
            'address': str,
            'reason': str,
            'amount': int,
            'description': str,
            'date': datetime.date
        }
        """
        
        entry_type = data.get('type')  # 'income' / 'outcome'
        entry_date = data.get('date')  # datetime.date
        
        # Cấp số phiếu
        voucher_no, voucher_year = FinanceController.get_next_voucher_no(entry_type, entry_date)

        # Gán vào data
        data['voucher_no'] = voucher_no
        data['voucher_year'] = voucher_year
        
        return IncomeOutcome.create(**data)

    @staticmethod
    def update_entry(entry_id, data):
        query = IncomeOutcome.update(**data).where(IncomeOutcome.id == entry_id)
        return query.execute()

    @staticmethod
    def get_entry(entry_id) -> IncomeOutcome:
        return IncomeOutcome.get_or_none(IncomeOutcome.id == entry_id)

    @staticmethod
    def get_entries(entry_type, month, year):
        from_date = datetime.date(year, month, 1)
        to_date = datetime.date(year + int(month / 12), month % 12 + 1, 1) - datetime.timedelta(days=1)
        return (
            IncomeOutcome
            .select()
            .where(
                (IncomeOutcome.type == entry_type) &
                (IncomeOutcome.date.between(from_date, to_date))
            )
            .order_by(IncomeOutcome.date)
        )

    @staticmethod
    def delete_entry(entry_id):
        return IncomeOutcome.delete().where(IncomeOutcome.id == entry_id).execute()

    @staticmethod
    def get_next_voucher_no(entry_type: str, entry_date: datetime.date) -> tuple[int, int]:
        year = entry_date.year
        with database.atomic():
            counter, created = VoucherCounter.get_or_create(
                type=entry_type,
                year=year,
                defaults={'last_no': 0}
            )
            # (Tùy chọn cho Postgres)
            try:
                (VoucherCounter
                .select()
                .where(VoucherCounter.id == counter.id)
                .for_update()
                .execute())
            except Exception:
                pass

            counter.last_no += 1
            counter.save()
            return counter.last_no, year
