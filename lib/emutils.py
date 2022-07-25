import email, ssl
import smtplib
#from smtplib import SMTP_SSL as SMTP #SSL connection
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import emconfig

def send_email(_sender_email, _receiver_email, _text):
    port = emconfig.port                
    password = emconfig.password        
    smtp_server = emconfig.smtp_server

    _result = False

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(_sender_email, password)
        _result = server.sendmail(_sender_email, _receiver_email, _text)

# error handling here --> https://stackoverflow.com/questions/44385652/add-senders-name-in-the-from-field-of-the-email-in-python#47823846    

    return _result



def create_message(sender_email, receiver_email, subject, body, filename1):

# Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails


    message.attach(MIMEText(body, "plain"))

#Attach log file
    with open(filename1, "rb") as attachment1:

        part1 = MIMEBase("application", "octet-stream")
        part1.set_payload(attachment1.read())

    encoders.encode_base64(part1)
    
    part1.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename1}",)

    message.attach(part1)
    text = message.as_string()
    return text


def create_multi_attachment_message(sender_email, receiver_email, subject, body, filename1, filename2, filename3):

# Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails


    message.attach(MIMEText(body, "plain"))

#Attach log file
    with open(filename1, "rb") as attachment1:

        part1 = MIMEBase("application", "octet-stream")
        part1.set_payload(attachment1.read())

    encoders.encode_base64(part1)
    
    part1.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename1}",)

    message.attach(part1)
    
#Attach download cronlog file
    with open(filename2, "rb") as attachment2:

        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment2.read())

    encoders.encode_base64(part2)
            
    part2.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename2}",)

    message.attach(part2)
    
 #Attach upload cronlog file
    with open(filename3, "rb") as attachment3:

        part3 = MIMEBase("application", "octet-stream")
        part3.set_payload(attachment3.read())

    encoders.encode_base64(part3)
            
    part3.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename3}",)

    message.attach(part3)
    
    text = message.as_string()
    return text



def assemble_email(log, subject):
    sender_email = emconfig.sender_email
    receiver_email = emconfig.receiver_email
    body = 'Log files attached.'    
    text = create_message(sender_email, receiver_email, subject, body, log)
    result = send_email(sender_email, receiver_email, text)
    return result



def assemble_multi_attachment_email(log, download_log, upload_log, subject):
    sender_email = emconfig.sender_email
    receiver_email = emconfig.receiver_email
    body = 'Log files attached. Search for Error in the upload log.'    
    text = create_message(sender_email, receiver_email, subject, body, log, download_log, upload_log,)
    result = send_email(sender_email, receiver_email, text)
    return result