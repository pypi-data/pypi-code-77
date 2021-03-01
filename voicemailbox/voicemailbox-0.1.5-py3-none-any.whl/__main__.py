import locale
import os

import dotenv

from voicemailbox import app
from voicemailbox import voicemail
from voicemailbox import email

dotenv.load_dotenv()
locale.setlocale(locale.LC_ALL, "")

# Run emails checking
email_manager = email.EmailManager(
    host=os.environ["VOICEMAILBOX_IMAP_SERVER"],
    email_address=os.environ["VOICEMAILBOX_EMAIL_ADDRESS"],
    password=os.environ["VOICEMAILBOX_EMAIL_PASSWORD"],
    dest_path=voicemail.VoicemailManager.PATH_NEW,
    attachment_pattern=voicemail.VoicemailManager.MAIL_PATTERN,
)

email_manager.start()

# Run kivy App
app.VoicemailBoxApp().run()
email_manager.end = True
email_manager.join()
