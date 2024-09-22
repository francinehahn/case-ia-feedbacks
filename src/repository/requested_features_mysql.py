from mysql.connector import Error

class RequestedFeaturesMySQL:
    def __init__(self, connection):
        self.connection = connection
        self.__table_name = 'requested_features'

    def insert_requested_feature(self, requested_feature):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"INSERT INTO {self.__table_name} (feature, code_id, feedback_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (requested_feature.get_feature(), requested_feature.get_code_id(), requested_feature.get_feedback_id()))
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()

    def get_requested_features(self, time_period:str):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"""
                SELECT rf.id, rf.feature, fc.code 
                FROM {self.__table_name} rf
                JOIN feature_codes fc
                ON rf.code_id = fc.id
                WHERE rf.created_at >= %s
            """
            cursor.execute(query, (time_period,))
            return cursor.fetchall()
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()
    
    def get_requested_features_percentage(self):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"""
                SELECT fc.code, COUNT(fc.code) / (SELECT COUNT(*) AS total_count FROM {self.__table_name}) * 100 
                FROM {self.__table_name} rf 
                JOIN feature_codes fc 
                ON fc.id = rf.code_id 
                GROUP BY code;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()