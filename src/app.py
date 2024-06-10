import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mysql.connector import Error
import smtplib
from marshmallow import ValidationError
from flask import Flask, jsonify, request, render_template
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

# web page
@app.route('/')
def index():
    try:
        report = feedback_service.feedbacks_report()
        return render_template('index.html', report=report)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422 
    except Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# endpoint that checks for spans, inserts the feedback into the db and returns the sentiment analysis by the llm
@app.route('/feedbacks', methods=['POST'])
def feedbacks():
    try:
        # get data from the client
        feedback_data = request.get_json()
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

    
# this function will be called every friday at 6PM to send the weekly report by email
def weekly_summary():
    try:
        feedback_service.weekly_summary()
        print('Email sent successfully.')
    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(str(e)) from e
    except Error as e:
        raise Error(str(e)) from e
    except Exception as e:
        raise Exception(str(e)) from e

if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(weekly_summary, 'cron', day_of_week='fri', hour=18, minute=00)
    scheduler.start()

    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()