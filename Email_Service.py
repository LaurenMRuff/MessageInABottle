# AUTHOR: Lauren Ruff
# Email: ruffl@oregonstate.edu
# Assignment: 6, minimum viable product (MVP)
# Due Date: February 14 2022
# Version: 1.0
# File: Email_Service.py
# Description: This will be the email service created for Ethan's Project. It will allow the user to email data to a
#              specified email address

import smtplib, imghdr
from email.message import EmailMessage


def generate_email(sender, recipient, subject, msg, file_path):

    new_msg = EmailMessage()
    new_msg['From'] = sender
    new_msg['To'] = recipient
    new_msg['Subject'] = subject
    new_msg.preamble = msg

    img_data = file_path.read()

    msg.add_attachment(file_path, maintype='image', subtype=imghdr.what(None, img_data))

    with smtplib.SMTP('localhost') as s:
        s.send_message(new_msg)
