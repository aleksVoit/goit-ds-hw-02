import sqlite3
from contextlib import contextmanager

database = './tasks.db'

@contextmanager
def create_connection(db_file: str):
    conn = sqlite3.connect(db_file)
    yield conn
    conn.rollback()
    conn.close()