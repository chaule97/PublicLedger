# myapp/db.py
import os, sys
from peewee import SqliteDatabase

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

DB_PATH = os.path.join(BASE_DIR, "app.db")
database = SqliteDatabase(DB_PATH)

if __name__ == "__main__":
    database.connect()