from src.repository.abstract_classes.feature_codes_repository import FeatureCodesRepository
from mysql.connector import Error

class FeatureCodesMySQL(FeatureCodesRepository):
    def __init__(self, connection):
        self.connection = connection
        self.__table_name = 'feature_codes'
        
    def get_codes(self):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            cursor.execute(f'SELECT * FROM {self.__table_name}')
            codes = cursor.fetchall()
            return codes
        except Error as e:
            print("Error while trying to connect to MySQL:", e)
            raise Error(str(e)) from e
        finally:
            cursor.close()
            self.connection.close()
    
    def insert_code(self, code):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"INSERT INTO {self.__table_name} (code) VALUES (%s)"
            cursor.execute(query, (code.get_code(),))
            connection_db.commit()
        except Error as e:
            print("Error while trying to connect to MySQL:", e)
            raise Error(str(e)) from e
        finally:
            cursor.close()
            self.connection.close()