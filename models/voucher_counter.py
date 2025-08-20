from peewee import Model, CharField, IntegerField
from db import database

from .income_outcome import IncomeOutcome

class VoucherCounter(Model):
    type = CharField(choices=IncomeOutcome.TYPE_CHOICES)  # 'income' hoặc 'outcome'
    year = IntegerField()
    last_no = IntegerField(default=0)

    class Meta:
        database = database
        table_name = "voucher_counter"
        indexes = (
            (('type', 'year'), True),  # unique
        )
