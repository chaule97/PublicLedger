# myapp/db.py
from peewee import SqliteDatabase

database = SqliteDatabase("app.db")

if __name__ == "__main__":
    database.connect()