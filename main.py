from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1fJfR22GDlk3C636qYsCiV42lajjZcAKEUUsB2uU3rEA' #get this from the url of your document,
#e.g: https://docs.google.com/document/d/1fJfR22GDlk3C636qYsCiV42lajjZcAKEUUsB2uU3rEA/edit, get the string between "/d/" and "/edit"


global document

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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

    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        global document
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        #print('The title of the document is: {}'.format(document.get('title')))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()


def get_word_count():
    wc = 0
    structural_objects = document.get('body').get('content')
    for so in structural_objects:
        paragraph = so.get("paragraph")
        if paragraph == None:
            continue
        paragraph_element = paragraph.get("elements")

        pg_content = paragraph_element[0]["textRun"]["content"] #raw text from the paragraph element
        pg_content = pg_content.replace("\n", "") #removing all the new line strings 

        wc += len(pg_content)
    return wc
