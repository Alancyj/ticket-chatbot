# ==== Emailing logic for the 4th option, requestion authorisation ====
# User should receive email after submitting the authorisation form

# Import smtplib for the actual sending function
import smtplib

# Import dotenv and os to store google pw separately
import dotenv
import os

# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SETUP
dotenv.load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
GOOGLE_PASSWORD = os.environ.get("GOOGLE_PASSWORD")

class email_class:
    def __init__(self, sender_email, recipent_email, message):
        self.sender_email = sender_email
        self.recipent_email = recipent_email
        self.message = message
        self.password = GOOGLE_PASSWORD

    def send_email(self):
        # Credentials
        message = MIMEMultipart()
        message['Subject'] = f'Authorisation Form Acknowledgement'
        message['From'] = self.sender_email
        message['To'] = self.recipent_email

        message.attach(MIMEText(self.message, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(message)
