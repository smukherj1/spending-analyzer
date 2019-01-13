from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
_SCOPES = "https://www.googleapis.com/auth/drive.metadata.readonly"


class DriveAPI(object):
    def __init__(self, credentials, folder_id):
        # The credentials.json file for Google Drive.
        self._credentials = credentials
        # The Google Drive Folder ID that has the Google Sheets
        # to be analyzed.
        self._folder_id = folder_id
        self._setup()

    def _build_query(self):
        return self._service.files().list(
            pageSize=12,
            fields="nextPageToken, files(id, name, mimeType)",
            q="'{}' in parents".format(self._folder_id))

    def query_files(self):
        results = self._build_query().execute()
        return results.get("files", [])

    def _setup(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage("token.json")
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self._credentials, _SCOPES)
            creds = tools.run_flow(
                flow, store, flags=tools.argparser.parse_args(args=[]))
        self._service = build("drive", "v3", http=creds.authorize(Http()))

