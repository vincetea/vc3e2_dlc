import csv
import json
import os
from pathlib import Path
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build


SECRET_FILE = "vc3e2_secret.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
OUTPUT_ROOT = Path("DLC Translation Files")
MAPPING_FILE = "dlc_sheets.json"
RANGE_EXPORT = "A:Z"


def make_sheets_service():
    if not os.path.exists(SECRET_FILE):
        raise SystemExit(f"{SECRET_FILE} is not within the vc3e2 folder! ")
    creds = service_account.Credentials.from_service_account_file(SECRET_FILE, scopes=SCOPES)
    return build ("sheets", "v4", credentials = creds)


def download_sheet_as_csv(service, spreadsheet_id: str, out_csv: Path):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=RANGE_EXPORT)
        .execute()
    )

    rows = result.get("values", [])

    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
def main():
    if not os.path.exists(MAPPING_FILE):
        raise SystemExit(f"{MAPPING_FILE} not found")

    service = make_sheets_service()

    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        dlc_map = json.load(f)

    for dlc_folder, files in dlc_map.items():
        for base_name, spreadsheet_id in files.items():
            out_csv = OUTPUT_ROOT / dlc_folder / f"{base_name}.csv"

            print(f"[DL] {dlc_folder} / {base_name}")
            download_sheet_as_csv(service, spreadsheet_id, out_csv)

            time.sleep(0.5)

    print("Done.")


if __name__ == "__main__":
    main()