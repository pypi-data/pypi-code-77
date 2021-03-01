import time
import threading
import socket
import email
from email import policy

from imapclient import IMAPClient, SocketTimeout
from imapclient.exceptions import IMAPClientAbortError, IMAPClientError

from voicemailbox import logger


class EmailManager(threading.Thread):

    def __init__(self,
                 host="",
                 email_address="",
                 password="",
                 dest_path=None,
                 attachment_pattern=None,
                 ):

        super().__init__()
        self.server_url = host
        self.email_address = email_address
        self.password = password
        self.dest_path = dest_path
        self.attachment_patern = attachment_pattern

        self.server = None
        self.time_start = 0.0

        self.end = False

    def connect(self):

        self.server = IMAPClient(host=self.server_url,
                                 use_uid=True,
                                 timeout=SocketTimeout(connect=15, read=60),
                                 )
        logger.info(f"Connecté au serveur IMAP {self.server_url}")

        self.server.login(self.email_address, self.password)
        logger.info(f"Authentifié sur le serveur "
                    f"en tant que {self.email_address}")

        self.server.select_folder('INBOX')
        logger.info("Boîte « INBOX » sélectionnée")

    def fetch_unseen_emails(self):

        search_result = self.server.search(
            criteria=("UNSEEN",)
        )

        emails = self.server.fetch(search_result, ("BODY[]",))

        # Loops on every found emails
        for uid, e in emails.items():
            logger.info("Traitement d'un nouveau courriel")
            message = email.message_from_bytes(e[b"BODY[]"],
                                               policy=policy.default,
                                               )
            # Loops on every attachment in an email
            for attachment in message.iter_attachments():

                logger.info(f"Pièce jointe de type "
                            f"{attachment.get_content_type()} identifiée")
                filename = attachment.get_filename()
                logger.info(f"Pièce jointe identifiée : {filename}")

                # Download attachment if it matches to the given pattern
                if (self.attachment_patern
                        and self.attachment_patern.match(filename)):
                    with open(self.dest_path / filename, mode="wb") as file:
                        file.write(attachment.get_content())

                    logger.info("La pièce jointe a été enregistrée.")

    def run(self):

        while True:

            try:

                if self.server is None:
                    logger.info(f"Connexion au serveur {self.server_url}")
                    self.connect()
                    self.fetch_unseen_emails()
                    self.time_start = time.monotonic()
                    self.server.idle()
                    logger.info("Passage en mode « idle »")

                # Start IDLE check
                responses = self.server.idle_check(timeout=30)

                if responses:
                    logger.info("Événement reçu du serveur")
                    self.server.idle_done()
                    self.fetch_unseen_emails()
                    self.server.idle()

                if self.end is True:
                    break

                if time.monotonic() - self.time_start >= 200:
                    logger.info("Renouvellement du mode « idle »")
                    self.time_start = time.monotonic()
                    self.server.idle_done()
                    self.server.idle()

            except (socket.gaierror, socket.timeout,
                    IMAPClientAbortError, IMAPClientError) as error:
                logger.warning(error)
                time.sleep(10)
                self.server = None
                continue

            except Exception as error:
                logger.error(f"{type(error)} - {error}")
                time.sleep(600)
                self.server = None
                continue
