import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import mysql.connector
from mysql.connector import Error
from src.config.db_config import DB_CONFIG

class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls, *args, **kwargs)
            cls._instance._connection = None
        return cls._instance
    
    def connect(self):
        if self._connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(**DB_CONFIG)
                if self.connection.is_connected():
                    print("The connection to MySQL has been established successfully!")
            except Error as e:
                print("Error while trying to connect to MySQL:", e)
                raise Error(str(e)) from e
        return self.connection

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("The connection to MySQL has been closed.")
