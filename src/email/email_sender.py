import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_mail import Message, Mail, BadHeaderError
from flask import current_app
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def send_alert(self, message:str):
        try:
            email_receivers_str = os.getenv('EMAIL_RECEIVERS')
            email_receivers_list = email_receivers_str.split(',')
            print('email receivers list: ', email_receivers_list)
            mail = Mail(current_app)
            msg = Message('Feedback Weekly Report', sender=os.getenv('EMAIL_SENDER'), recipients=email_receivers_list)
            msg.body = message
            mail.send(msg)
        except BadHeaderError as e:
            raise BadHeaderError(str(e)) from e
        except Exception as e:
            raise Exception(str(e)) from e