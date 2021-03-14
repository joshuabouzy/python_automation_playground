import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from decouple import config

class EmailBot:
    def send_email(self, receiver_address, 
                   email_subject, email_content,
                   file_path):
        #Sets up the MIME object
        message = MIMEMultipart()
        message['From'] = config('GMAIL_USERNAME')
        message['To'] = receiver_address
        message['Subject'] = email_subject

        #The body and attachments for the email
        message.attach(MIMEText(email_content, 'plain'))
        
        #Opens file that will be attached
        attachment = open(file_path, 'rb')
        
        #Create an instance of mimebase
        mimebase = MIMEBase('application', 'octet-stream')
        
        #Encodes the attachment into base64
        mimebase.set_payload((attachment).read())
        encoders.encode_base64(mimebase)
        mimebase.add_header('Content-Disposition',
                            'attachment; filename = %s' % file_path)

        message.attach(mimebase)
                
        #Create SMTP session for sending the email
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(
            config("GMAIL_USERNAME"),
            config("GMAIL_PASSWORD"))
        text = message.as_string()
        session.sendmail(
            config("GMAIL_USERNAME"),
            receiver_address, text)
        session.quit()