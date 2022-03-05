import sqlite3
import os

import backend.query

DIR = os.path.split(os.path.realpath(__file__))[0]

DB_NAME = os.path.join(DIR, "sunnytots.db")


class Backend:
    def __init__(self, db_name=DB_NAME):
        self.__db_name = db_name
        self.__connection = sqlite3.connect(self.__db_name)
        self.__history = 0
        self.__add_savepoint()

    def handle_query(self, query):
        qtext, param = query.generate_query()
        try:
            result = query.execute(self.__connection)
            if query.changed_db():
                self.__add_savepoint()
        except sqlite3.Error:
            print(qtext, param)
            raise
        return result

    def commit(self):
        self.__connection.commit()

    def rollback(self):
        self.__connection.rollback()

    def __add_savepoint(self):
        self.__history += 1
        self.__connection.execute(f"SAVEPOINT s{self.__history}")

    def undo(self):
        if self.__history > 1:
            self.__history -= 1
            self.__connection.execute(f"ROLLBACK TO s{self.__history}")

    def gen_new_query(self, type_):
        if type_ == "add":
            return backend.query.AddQuery()
        elif type_ == "get":
            return backend.query.GetQuery()
        elif type_ == "change":
            return backend.query.ChangeQuery()
        elif type_ == "remove":
            return backend.query.RemoveQuery()
        else:
            return backend.query.NullQuery()
