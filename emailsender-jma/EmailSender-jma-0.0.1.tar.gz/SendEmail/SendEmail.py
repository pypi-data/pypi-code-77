import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import config of credentials from local file
import sys
sys.path.append('/Users/jinghanma/Helium10/utility_jma/util_config') # user needs to change the path to their own path
from oauth_email_config import *

# from logger_jm import mylogger


def send_email(project, email_subject, msg, attachment_path=None, attachment_name=None):

    # logger = mylogger(log_file_name='testjm.log')

    # email server config
    smtp_server = 'smtp.gmail.com'
    port = 587

    # email concat config
    project_id = oauth_emails()[project]

    sender = project_id['sender_email']
    pwd = project_id['password']
    receivers = project_id['receiver_email']

    # create email head
    email = MIMEMultipart()
    email["From"] = sender
    email["To"] = ', '.join(receivers)
    email["Subject"] = email_subject

    # add msg body to email
    email.attach(MIMEText(msg, "plain"))

    # add attachment to email if there is one
    if attachment_path is not None:
        attachment_obj = open(os.path.join(attachment_path, attachment_name), "rb")  # open the file
        report = MIMEBase("application", "octate-stream")
        report.set_payload(attachment_obj.read())
        encoders.encode_base64(report)

        # add name for the attachment
        report.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_name}",
        )
        email.attach(report)

    text = email.as_string()

    # create SMTP session for sending the mail
    session = smtplib.SMTP(smtp_server, port)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender, pwd)  # login with mail_id and password
    # logger.info('Start Sending emails:')
    try:
        for people in receivers:
            session.sendmail(sender, people, text)
            print('Mail delivered for receiver: {}'.format(people))
            # logger.info('Mail delivered for receiver: {}'.format(people))
    except:
        # logger.error('FAILURE during mail delivering')
        print('failed to deliver')
    session.quit()


if __name__ == '__main__':
    pass

    # there is attachment
    # send_email(project='test',
    #            email_subject='let me test this',
    #            msg="""
    #            Hello from the other side
    #            I must have called a thousand times
    #            oh~~~ oh~~~
    #            """,
    #            attachment_path="/Users/jinghanma/Helium10/Adhoc/audit_segment",
    #            attachment_name="audit_segment_20210115.csv")

    # without attachment
    # send_email(project='test',
    #                    email_subject='log Success!!!',
    #                    msg="""
    #                    Success doesn't need attachment
    #                    """)