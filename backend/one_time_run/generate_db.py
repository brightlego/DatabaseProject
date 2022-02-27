import sqlite3
import os

DIR = os.path.split(os.path.realpath(__file__))[0]

DB_NAME = os.path.join(DIR, "..", "sunnytots.db")
SQL_STATEMENTS = "SQLstatements.sql"

connection = sqlite3.connect(DB_NAME)

with open(SQL_STATEMENTS, "rt") as f:
    statements = f.read()
    connection.executescript(statements)

connection.commit()
connection.close()
