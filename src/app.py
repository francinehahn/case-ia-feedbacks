import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mysql.connector import Error
from marshmallow import ValidationError
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from service.feedback_service import FeedbackService
from repository.implementations.feedback_mysql import FeedbackMySQL
from repository.implementations.requested_features_mysql import RequestedFeaturesMySQL
from repository.implementations.feature_codes_mysql import FeatureCodesMySQL
from db.connection import DatabaseConnection
from ai.implementations.command_r_plus import CommandRplus
from email_sender.email_sender import EmailSender
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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


@app.route('/feedbacks_report', methods=['GET'])
def feedbacks_report():
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
        report = feedback_service.feedbacks_report()
        return jsonify(report), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422 
    except Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# this function will call the weeklySummary endpoint all fridays at 6PM
def weekly_summary():
    with app.app_context():
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
        except Error as e:
            print(str(e))
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(weekly_summary, 'cron', day_of_week='fri', hour=18, minute=00)
    scheduler.start()

    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()