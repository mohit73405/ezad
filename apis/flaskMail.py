from flask import Flask
from flask_mail import Mail,Message
mail_app = Flask(__name__)


# mail = Mail(mail_app)

# class flaskMail:
# def send_email(from_email,to_email,subject):
#     msg = Message("Hello",
#                   sender=from_email,
#                   recipients=[to_email])
#     msg.html = "<b>testing</b>"
#     mail.send(msg)

