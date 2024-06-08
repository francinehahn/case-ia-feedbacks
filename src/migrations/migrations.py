import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mysql.connector import Error
from db.connection import DatabaseConnection

def create_tables():
    try:
        db_connection = DatabaseConnection()
        connection = db_connection.connect()
        cursor = connection.cursor()
            
        # Create feedbacks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedbacks (
                id CHAR(36) PRIMARY KEY,
                feedback TEXT,
                sentiment ENUM('POSITIVO', 'NEGATIVO', 'INCONCLUSIVO')
            );
        """)

        # Create table feature_codes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feature_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(255)
            );
        """)

        # Create table requested_features
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requested_features (
                id INT AUTO_INCREMENT PRIMARY KEY,
                feature VARCHAR(255),
                code_id INT,
                feedback_id CHAR(36),
                FOREIGN KEY (code_id) REFERENCES feature_codes(id),
                FOREIGN KEY (feedback_id) REFERENCES feedbacks(id)
            );
        """)

        print("Tables created successfully!")
    
    except Error as e:
        print("Connection Error: ", e)
    
    finally:
        db_connection.close()
        print("The connection has been closed.")

if __name__ == '__main__':
    create_tables()
