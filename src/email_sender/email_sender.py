import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class EmailSender():
    def __init__(self):
        # Email configuration
        self.sender_email = os.getenv("MAIL_USERNAME")
        self.sender_password = os.getenv("MAIL_PASSWORD")
        self.recipients_emails = os.getenv("EMAIL_RECEIVERS")
        self.smtp_server = os.getenv("MAIL_SERVER")
        self.smtp_port = 587

    def send(self, email:str):
        try:
            # get all the emails included in the string
            recipients = self.recipients_emails.split(',')
            print('recipients: ', recipients)
            
            # Create the message
            message = EmailMessage()
            message.set_content(email)
            message['From'] = self.sender_email
            message['To'] = recipients
            message['Subject'] = 'Feedback Weekly Report'

            # send the email
            smtp_obj = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp_obj.starttls()
            smtp_obj.login(self.sender_email, self.sender_password)
            smtp_obj.send_message(message)
            smtp_obj.quit()
        except smtplib.SMTPException as e:
            raise smtplib.SMTPException(str(e))
