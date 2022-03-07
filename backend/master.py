"""The backend master file"""

import sqlite3
import os

import backend.query

# Get the directory of this file
DIR = os.path.split(os.path.realpath(__file__))[0]

# Get the database
DB_NAME = os.path.join(DIR, "sunnytots.db")


class Backend:
    """The backend master.

    Attributes:
        Private:
            __db_name (str)
                -- The database name
            __connection (sqlite3.Connection)
                -- The connection to the database
            __current_query_id (int)
                -- The ID of the most recent query

    Methods:
        Magic:
            __init__(db_name:str=DB_NAME)
        Public:
            handle_query(query: backend.query.Query)
                -- handles a query
            commit() -> None
                -- Commits the database
            rollback() -> None
                -- Rolls back the database
            close() -> None
                -- Closes the database
            undo() -> None
                -- Undoes the database one step
            gen_new_query() -> backend.query.Query
                -- Generates a new query
        Private:
            __add_savepoint() -> None
                -- Adds a savepoint to the database
    """

    def __init__(self, db_name=DB_NAME):
        """The constructor for Backend

        Arguments:
            None

        Keyword Arguments:
            db_name (str) default DB_NAME
                -- The name of the database

        Returns:
            None
        """
        self.__db_name = db_name

        # Create a connection
        self.__connection = sqlite3.connect(self.__db_name)
        self.__current_query_id = 0

        # Add the first save point
        self.__add_savepoint()

    def handle_query(self, query):
        """Handles a query

        Arguments:
            query (backend.query.Query)
                -- The query to handle

        Returns:
            None
        """
        try:
            # Execute the query
            result = query.execute(self.__connection)

            # If the query might have changed the database, add a savepoint
            if query.changed_db():
                self.__add_savepoint()
        # In the case of an error
        except sqlite3.Error:
            # Get the query text and the parameters for debugging and raise
            qtext, param = query.generate_query()
            print(qtext, param)
            raise

        # Return the result
        return result

    def commit(self):
        """Commits the database"""
        self.__connection.commit()

        # Reset the savepoints
        self.__current_query_id = 0
        self.__add_savepoint()

    def rollback(self):
        """Rolls back the database"""
        self.__connection.rollback()

        # Reset the savepoints

        self.__current_query_id = 0
        self.__add_savepoint()

    def close(self):
        """Closes the database"""
        self.__connection.close()

    def __add_savepoint(self):
        """Adds a savepoint to the database

        Arguments:
            None

        Returns:
            None
        """
        # Increment the current query it
        self.__current_query_id += 1

        # Add a savepoint of that ID (has a prefix of s as otherwise sqlite
        # complains)
        self.__connection.execute(f"SAVEPOINT s{self.__current_query_id}")

    def undo(self):
        """Undoes the previous change to the database

        Arguments:
            None

        Returns:
            None
        """

        # If there have been any changes to the database
        if self.__current_query_id > 1:
            # Decrement it
            self.__current_query_id -= 1

            # Roll back to the previous savepoint
            self.__connection.execute(f"ROLLBACK TO s{self.__current_query_id}")

    def gen_new_query(self, type_, limit):
        """Generates a new query of type `type_`

        Arguments:
            type_ (str)
                -- The type of query
            limit (int)
                -- The limit of the query

        Returns:
            query (backend.query.Query)
                -- The new query
        """

        # Make the type case insensitive
        type_ = type_.lower()

        # Return a query of that type
        if type_ == "add":
            query = backend.query.AddQuery
        elif type_ == "get":
            query = backend.query.GetQuery
        elif type_ == "change":
            query = backend.query.ChangeQuery
        elif type_ == "remove":
            query = backend.query.RemoveQuery

        # If an invalid type is specified, return a null query
        else:
            query = backend.query.NullQuery

        if limit is None:
            return query()
        else:
            return query(limit=limit)
