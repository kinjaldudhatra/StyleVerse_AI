import sqlite3
from contextlib import closing

from config import Config


def get_connection():
    """Return a SQLite connection that returns rows as dictionary-like objects."""
    connection = sqlite3.connect(Config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def fetch_all(query, params=()):
    """Run a SELECT query and return all matching rows."""
    with closing(get_connection()) as connection:
        return connection.execute(query, params).fetchall()


def fetch_one(query, params=()):
    """Run a SELECT query and return the first matching row, or None."""
    with closing(get_connection()) as connection:
        return connection.execute(query, params).fetchone()
