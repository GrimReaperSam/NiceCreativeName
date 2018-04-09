#!/usr/bin/python3
from __future__ import print_function
import httplib2
import httplib2shim
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client.client import GoogleCredentials
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Python OCR'


def get_credentials():
    credential_path = os.path.join("./", 'google-ocr-credential.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('credential_path:' + credential_path)
    return credentials


def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2shim.Http())
    service = discovery.build('drive', 'v3', http=http)
    mime = 'application/vnd.google-apps.document'

    for root, dirs, files in os.walk("Pdf"):
        for file in files:
            if file.endswith(".pdf"):
                file_name = os.path.splitext(file)[0]

                res = service.files().create(
                    body={
                        'name': file,
                        'mimeType': mime
                    },
                    media_body=MediaFileUpload("Pdf/" + file, mimetype=mime, resumable=True)
                ).execute()

                downloader = MediaIoBaseDownload(
                    io.FileIO("Text/" + file_name + ".txt", 'wb'),
                    service.files().export_media(fileId=res['id'], mimeType="text/plain")
                )
                done = False
                while done is False:
                    status, done = downloader.next_chunk()

                service.files().delete(fileId=res['id']).execute()


if __name__ == '__main__':
    main()
