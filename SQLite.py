
import sqlite3

class LibDB:
    def __init__ (self, dbName = 'Library.db'):
        super().__init__()
        self.dbName = dbName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                Book_ID INTEGER PRIMARY KEY,
                Title TEXT,
                Author TEXT,
                Genre TEXT,
                Availability_Status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()   

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Employees (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    role TEXT,
                    gender TEXT,
                    status TEXT)''')
        self.commit_close()

































