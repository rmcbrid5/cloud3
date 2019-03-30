import requests
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendit():
    port = 465  # For SSL
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        password = 'R1@namcb'
        server.login("msgservice112@gmail.com", password)
        sender_email = "msgservice112@gmail.com"
        receiver_email = "rmcbrid5@uwo.ca"
        # TODO: Send email here
        subject = "Message Service Failing"
        body = "The message API is not responding on port 50001, please investigate."
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

try:
    a = requests.get('http://localhost:50001/retreive')
    print(a.text)
    if ("Error" or "error") in a.text:
        sendit()
except:
    sendit()