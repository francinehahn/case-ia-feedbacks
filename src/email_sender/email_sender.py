import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
from dotenv import load_dotenv
from flask_mail import Message, Mail, BadHeaderError

load_dotenv()

class EmailSender:
    def __init__(self, app):
        self.app = app

    def send(self, message:str):
        try:
            email_receivers_str = os.getenv('EMAIL_RECEIVERS')
            email_receivers_list = email_receivers_str.split(',')
            mail = Mail(self.app)
            msg = Message('Feedback Weekly Report', sender=os.getenv('EMAIL_SENDER'), recipients=email_receivers_list)
            msg.body = message
            mail.send(msg)
        except BadHeaderError as e:
            raise BadHeaderError(str(e)) from e
        except Exception as e:
            raise Exception(str(e)) from e