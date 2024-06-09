from src.repository.abstract_classes.feedback_repository import FeedbackRepository
from mysql.connector import Error

class FeedbackMySQL(FeedbackRepository):
    def __init__(self, connection):
        self.connection = connection
        self.__table_name = 'feedbacks'
        
    def insert_feedback(self, feedback):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"INSERT INTO {self.__table_name} (id, feedback, sentiment) VALUES (%s, %s, %s)"
            cursor.execute(query, (feedback.get_id(), feedback.get_feedback(), feedback.get_sentiment()))
            connection_db.commit()
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()
            self.connection.close()
            
    def get_feedback_by_id(self, feedback_id:str):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"SELECT * FROM {self.__table_name} WHERE id = %s"
            cursor.execute(query, (feedback_id,))
            result = cursor.fetchone()
            return result
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()
            self.connection.close()
            
    def get_feedbacks_sentiment_percentage(self, time_period:str):
        try:
            connection_db = self.connection.connect()
            cursor = connection_db.cursor()
            query = f"""
                SELECT sentiment, COUNT(*) * 100 / (SELECT COUNT(*) FROM {self.__table_name} WHERE created_at >= %s) AS percentage
                FROM {self.__table_name}
                WHERE created_at >= %s
                GROUP BY sentiment
            """
            cursor.execute(query, (time_period, time_period))
            result = cursor.fetchall()
            return result
        except Error as e:
            raise Error(str(e)) from e
        finally:
            cursor.close()
            self.connection.close()