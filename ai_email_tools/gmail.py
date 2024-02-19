import imaplib
import email
from email.header import decode_header

class EmailReader:
    def __init__(self, username, password, server, port):
        self.mail = imaplib.IMAP4_SSL(server, port)
        self.mail.login(username, password)

    def get_inbox(self):
        self.mail.select("inbox")
        result, data = self.mail.uid('search', None, "ALL")
        email_ids = data[0].split()
        email_ids = email_ids[::-1]  # newest emails first

        for i in email_ids:
            result, data = self.mail.uid('fetch', i, '(BODY[HEADER.FIELDS (SUBJECT)])')
            raw_email = data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)
            print(decode_header(email_message['Subject'])[0])

    def close_connection(self):
        self.mail.logout()