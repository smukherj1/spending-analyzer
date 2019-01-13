from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
# Read, write and manage permissions.
_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


class SheetsAPI(object):
    def __init__(self, credentials):
        self._credentials = credentials
        self._setup()

    def _setup(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('sheets.token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self._credentials, _SCOPES)
            creds = tools.run_flow(
                flow, store, flags=tools.argparser.parse_args(args=[]))
        self._service = build('sheets', 'v4', http=creds.authorize(Http()))

    def _build_query(self, doc_id, range_name):
        # Call the Sheets API
        sheet = self._service.spreadsheets()
        return sheet.values().get(spreadsheetId=doc_id, range=range_name)

    def query_doc(self, doc_id):
        # Column A: Item name
        # Column B: Price
        # Column C: Category
        # Column D: Date
        # Column E: Notes
        # First item on row 6
        base_row = 6
        num_rows = 20
        values = []
        while True:
            range_name = "A{}:D{}".format(base_row, base_row + num_rows - 1)
            base_row += num_rows
            result = self._build_query(doc_id, range_name).execute()
            query_values = result.get("values", [])
            if not query_values:
                break
            for row in query_values:
                item, expense, category, date = row
                values.append({
                    "item": item,
                    "expense": expense,
                    "category": category,
                    "date": date
                })
        return values
