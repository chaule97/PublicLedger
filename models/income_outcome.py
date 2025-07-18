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
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = database
        table_name = "income_outcome"