import os
import sys

sys.path.insert(0, "src/vendor")
import gspread

SPREADSHEET_NAME = os.environ.get("SPREADSHEET_NAME", "gastos-test")
WORKSHEET_INDEX = int(os.environ.get("WORKSHEET_INDEX", 0))


class SpreadsheetsManager:
    SCOPE = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file"
    ]

    def __init__(self) -> None:
        self.credentials = {
            "type": os.environ.get("GSHEETS_TYPE"),
            "project_id": os.environ.get("GHSEETS_PROJECT_ID"),
            "private_key_id": os.environ.get("GSHEETS_PRIVATE_KEY_ID"),
            # the termination char is treated as literal, need to unpad it
            "private_key": os.environ.get("GSHEETS_PRIVATE_KEY").replace("\\n", "\n"),
            "client_email": os.environ.get("GSHEETS_CLIENT_EMAIL"),
            "client_id": os.environ.get("GSHEETS_CLIENT_ID"),
            "auth_uri": os.environ.get("GSHEETS_AUTH_URI"),
            "token_uri": os.environ.get("GSHEETS_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("GSHEETS_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.environ.get("GSHEETS_CLIENT_X509_CERT_URL"),
        }

    def authorize_credentials(self):
        # print(f"## SpreadsheetsManager: Authorizing creds: {self.credentials}...")
        self.client = gspread.service_account_from_dict(self.credentials)

    def get_sheet(self, spreadsheet_name: str = SPREADSHEET_NAME, worksheet: int = WORKSHEET_INDEX):
        # print(f"## SpreadsheetsManager: Opening sheet {spreadsheet_name}/{worksheet} ...")
        spreadsheet = self.client.open(spreadsheet_name)
        return spreadsheet.get_worksheet(worksheet)

    def add_spending(self, s_date, s_type, s_category1, s_category2, s_dest, s_amount, s_currency, exch_rate, spreadsheet=None):
        print(f"## SpreadsheetsManager: Adding spending {s_date}|{s_type}|{s_category1} ...")
        if not spreadsheet:
            spreadsheet = self.get_sheet()
        spreadsheet.append_row([s_date, s_type, s_category1, s_category2, s_dest, s_amount, s_currency, exch_rate])
