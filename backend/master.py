import sqlite3

DB_NAME = "sunnytots.db"

class Backend:
    def __init__(self,db_name=DB_NAME):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
    
    def handle_data(self, query):
        pass