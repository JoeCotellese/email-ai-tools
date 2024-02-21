import base64
import logging
import os
import os.path

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# setup logging so that it only logs from this app and not 
# from imported modules
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Gmail:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
        self.creds = None

    def authenticate(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.scopes)
                self.creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def list_labels(self):
        try:
            service = build("gmail", "v1", credentials=self.creds)
            results = service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])

            if not labels:
                logger.info("No labels found.")
                return

            for label in labels:
                logger.info(label["name"])

        except HttpError as error:
            logger.error(f"An error occurred: {error}")

    def get_messages(self, mailbox):
        try:
            service = build("gmail", "v1", credentials=self.creds)
            results = (
                service.users()
                .messages()
                .list(userId="me", labelIds=mailbox)
                .execute()
            )
            messages = results.get("messages", [])

            if not messages:
                print("No messages found.")
                return

        except HttpError as error:
            print(f"An error occurred: {error}")

        return messages

    def get_subject(self, message_id):
        message = {}
        try:
            service = build("gmail", "v1", credentials=self.creds)
            message = (
                service.users()
                .messages()
                .get(userId="me", id=message_id)
                .execute()
            )
        except HttpError as error:
            print(f"An error occurred: {error}")
        
        # add the subject line to the dictionary
        for header in message["payload"]["headers"]:
            if header["name"] == "Subject":
                return header["value"]

    def read_message(self, message_id):
        # get the list of recipients for the message id
        # and store it into a "message" dictionary
        message = {}
        try:
            service = build("gmail", "v1", credentials=self.creds)
            message = (
                service.users()
                .messages()
                .get(userId="me", id=message_id)
                .execute()
            )
        except HttpError as error:
            print(f"An error occurred: {error}")
       
        # add the subject line to the dictionary
        for header in message["payload"]["headers"]:
            if header["name"] == "Subject":
                message["subject"] = header["value"]
                break
                # Decode the email body
    # Initialize attachment list
        message['attachments'] = []

        # Function to process parts
        def process_parts(parts, container):
            for part in parts:
                part_body = part.get('body', {})
                headers = part.get('headers', [])
                part_headers = {header['name']: header['value'] for header in headers}

                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    body_data = part_body.get('data', '')
                    body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    container[part['mimeType']] = body
                elif 'parts' in part:
                    # Recursively process subparts
                    process_parts(part['parts'], container)
                elif part['mimeType'] == 'application/octet-stream':
                    attachment_id = part_body.get('attachmentId')
                    attachment = service.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute()
                    attachment_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                    filename = part_headers.get('filename', 'attachment')
                    container['attachments'].append({'filename': filename, 'data': attachment_data})

        # Check if the email is multipart
        parts = message.get('payload', {}).get('parts', [])
        email_content = {'text/plain': '', 'text/html': '', 'attachments': []}
        process_parts(parts, email_content)

        # Update message dictionary with processed content
        message.update(email_content)
        message = self.clean_message(message)
        return message


    def clean_message(self, message):
        # clean the HTML message by removing any style information
        # within HTML tags
        soup = BeautifulSoup(message["text/html"], "html.parser")
        for tag in soup(["style"]):
            tag.decompose()
        message["text/html"] = soup.get_text()
        return message

        
    def decode_body(self, body):
        pass
