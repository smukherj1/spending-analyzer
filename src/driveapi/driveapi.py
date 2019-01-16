from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os

# If modifying these scopes, delete the file token.json.
# Read, write and manage permissions.
_SCOPES = "https://www.googleapis.com/auth/drive"


class DriveAPI(object):
    def __init__(self, credentials, folder_id, cache_dir):
        # The credentials.json file for Google Drive.
        self._credentials = credentials
        # The Google Drive Folder ID that has the Google Sheets
        # to be analyzed.
        self._folder_id = folder_id
        self._cache_dir = cache_dir
        self._setup()

    def _build_query(self):
        return self._service.files().list(
            # We expect a max of 12 expense files per year.
            pageSize=12,
            fields="nextPageToken, files(id, name, mimeType)",
            # Only search for files in the specified folder.
            q="'{}' in parents".format(self._folder_id) + " and " +
            # Only look for Google Sheets files.
            "mimeType contains 'application/vnd.google-apps.spreadsheet'")

    def query_files(self):
        results = self._build_query().execute()
        return results.get("files", [])

    def delete_file(self, file_id):
        return self._service.files().delete(fileId=file_id).execute()

    def create_output_file(self, name):
        return self._service.files().create(
            fields="id",
            body={
                "name": name,
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "parents": [self._folder_id]
            }).execute()

    def _setup(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage(os.path.join(self._cache_dir, "drive.token.json"))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self._credentials, _SCOPES)
            creds = tools.run_flow(
                flow, store, flags=tools.argparser.parse_args(args=[]))
        self._service = build("drive", "v3", http=creds.authorize(Http()))
