from twilio.rest import Client
import smtplib
import os


ACC_SID = os.environ.get("ACC_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TW_NUM")

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
PWD = os.environ.get("PWD")

class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""
    def __init__(self):
        self.client = Client(ACC_SID, AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            from_=TWILIO_NUMBER,
            to=os.environ.get("TO_NUM"),
            body=message
        )
        print(message.status)

    def send_email(self, email, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=SENDER_EMAIL, password=PWD)
            connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=email,
                                msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                                )

