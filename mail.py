import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def list_last_200_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=200).execute()
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        sender = [header['value'] for header in headers if header['name'] == 'From'][0]
        subject = [header['value'] for header in headers if header['name'] == 'Subject'][0]
        print(f"Sender: {sender}, Subject: {subject}")


if __name__ == '__main__':
    import os.path

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        creds = get_credentials()
    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    list_last_200_emails(service)
