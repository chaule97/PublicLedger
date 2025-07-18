# controllers/finance_controller.py
import datetime
from models import IncomeOutcome


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
        return IncomeOutcome.create(**data)

    @staticmethod
    def update_entry(entry_id, data):
        query = IncomeOutcome.update(**data).where(IncomeOutcome.id == entry_id)
        return query.execute()

    @staticmethod
    def get_entry(entry_id):
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
