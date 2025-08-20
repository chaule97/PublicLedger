import datetime
from peewee import Model, CharField, IntegerField, DateField, DateTimeField

from db import database

class IncomeOutcome(Model):
    INCOME = 'income'
    OUTCOME = 'outcome'

    TYPE_CHOICES = ((INCOME, 'Income'), (OUTCOME, 'Outcome'))

    type = CharField(choices=TYPE_CHOICES)
    name = CharField()
    address = CharField(null=True)
    reason = CharField(null=True)
    amount = IntegerField()
    description = CharField(null=True)
    date = DateField()
    voucher_year = IntegerField(default=lambda: datetime.date.today().year, null=True)
    voucher_no = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = database
        table_name = "income_outcome"