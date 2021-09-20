import email, ssl
import smtplib
#from smtplib import SMTP_SSL as SMTP #SSL connection
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(_sender_email, _receiver_email, _text):
    port = 465  # For SSL
    password = '2U!3yYwwR'  # input("Type your password and press enter: ")
    _result = False
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(_sender_email, password)
        _result = server.sendmail(_sender_email, _receiver_email, _text)

# error handling here --> https://stackoverflow.com/questions/44385652/add-senders-name-in-the-from-field-of-the-email-in-python#47823846    

    return _result



def create_message(sender_email, receiver_email, subject, body, filename):

# Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
    message.attach(MIMEText(body, "plain"))

# Open PDF file in binary mode
    with open(filename, "rb") as attachment:
# Add file as application/octet-stream
# Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

# Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    return text



def assemble_email(filename, subject):
    sender_email = "pps.smtp@gmail.com"  # "Your name <Your email>"
    receiver_email = "wplaird@bigpond.com"
    body = 'Log file attached ' + filename
    text = create_message(sender_email, receiver_email, subject, body, filename)
    result = send_email(sender_email, receiver_email, text)
    return result

