import sqlite3


# Database class to handle the SQLite database path and connecting to it.
class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    # Connect to the SQLite database via the provided path.
    def connect(self):
        return sqlite3.connect(self.db_path)
