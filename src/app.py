import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mysql.connector import Error
from marshmallow import ValidationError
from flask import Flask, jsonify, request
from service.feedback_service import FeedbackService
from repository.implementations.feedback_mysql import FeedbackMySQL
from repository.implementations.requested_features_mysql import RequestedFeaturesMySQL
from repository.implementations.feature_codes_mysql import FeatureCodesMySQL
from db.connection import DatabaseConnection
from ai.implementations.command_r_plus import CommandRplus
from email.email_sender import EmailSender
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# email config
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = 587  # SMTP port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

@app.route('/feedbacks', methods=['POST'])
def feedbacks():
    try:
        # get data from the client
        feedback_data = request.get_json()
        
        # database connection
        db_connection = DatabaseConnection()
        
        # repository layer
        feedback_repository = FeedbackMySQL(connection=db_connection)
        requested_features_repository = RequestedFeaturesMySQL(connection=db_connection)
        feature_codes_repository = FeatureCodesMySQL(connection=db_connection)
        
        # AI
        llm = CommandRplus()
        
        # service layer
        feedback_service = FeedbackService(
            feedback_repository=feedback_repository,
            requested_features_repository=requested_features_repository,
            feature_codes_repository=feature_codes_repository,
            llm=llm
        )
        feedback = feedback_service.feedbacks(feedback_data)
        
        return jsonify(feedback), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 422 
    except ValidationError as e:
        return jsonify({"error": str(e)}), 422 
    except Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/weeklySummary', methods=['GET'])
def weekly_summary():
    try:
        # database connection
        db_connection = DatabaseConnection()

        # repository layer
        feedback_repository = FeedbackMySQL(connection=db_connection)
        requested_features_repository = RequestedFeaturesMySQL(connection=db_connection)
        feature_codes_repository = FeatureCodesMySQL(connection=db_connection)

        # AI
        llm = CommandRplus()
        
        # email sender
        email_sender = EmailSender()

        # service layer
        feedback_service = FeedbackService(
            feedback_repository=feedback_repository,
            requested_features_repository=requested_features_repository,
            feature_codes_repository=feature_codes_repository,
            llm=llm,
            email_sender=email_sender
        )
        feedback_service.weekly_summary()

        return jsonify({'message': 'The email has been sent successfully.'}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except ValidationError as e:
        return jsonify({"error": str(e)}), 422
    except Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)