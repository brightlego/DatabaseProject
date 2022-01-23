import sqlite3

DB_NAME = "sunnytots.db"
SQL_STATEMENTS = "SQLstatements.sql"

connection = sqlite3.connect(DB_NAME)

with open(SQL_STATEMENTS, "rt") as f:
    statements = f.read()
    connection.executescript(statements)

connection.commit()
connection.close()
