# models/setting.py
from peewee import Model, CharField

from db import database


class Setting(Model):
    key = CharField(unique=True)
    value = CharField()

    class Meta:
        database = database
        table_name = "settings"

    @classmethod
    def get_value(cls, key, default=None):
        setting = cls.get_or_none(cls.key == key)
        return setting.value if setting else default

    @classmethod
    def set_value(cls, key, value):
        cls.insert(key=key, value=value).on_conflict_replace().execute()
