from src.repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository
from mysql.connector import Error

class RequestedFeaturesMySQL(RequestedFeaturesRepository):
    def __init__(self, connection):
        self.connection = connection
        self.__table_name = 'requested_features'
        
    def insert_requested_feature(self, requested_feature):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"INSERT INTO {self.__table_name} (feature, code_id, feedback_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (requested_feature.get_feature(), requested_feature.get_code_id(), requested_feature.get_feedback_id()))
            connection_db.commit()
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()
            self.connection.close()

    def get_requested_features(self, time_period:str):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = """
                SELECT rf.id, rf.feature, fc.code 
                FROM requested_features rf
                JOIN feature_codes fc ON rf.code_id = fc.id
                WHERE rf.created_at >= %s
            """
            cursor.execute(query, (time_period,))
            return cursor.fetchall()
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()
            self.connection.close()