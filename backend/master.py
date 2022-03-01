import sqlite3
import backend.query
import os
import copy

DIR = os.path.split(os.path.realpath(__file__))[0]

DB_NAME = os.path.join(DIR, "sunnytots.db")


class Backend:
    def __init__(self, db_name=DB_NAME):
        self.__db_name = db_name
        self.__connection = sqlite3.connect(self.__db_name)
        self.__history = []

    def handle_query(self, query):
        self.__history.append(copy.deepcopy(query))
        qtext, param = query.generate_query()
        print(qtext, param)
        try:
            result = self.__connection.execute(qtext, param)
        except sqlite3.Error:
            print(qtext, param)
            raise
        return result

    def commit(self):
        self.__connection.commit()

    def rollback(self):
        self.__connection.rollback()

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
