import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

def test_connection():
    try:
        print("1. Loading environment variables...")
        load_dotenv()
        sheet_id = os.getenv('SHEET_ID')
        creds_file = os.getenv('GOOGLE_CREDENTIALS_FILE')
        print(f"Sheet ID: {sheet_id}")
        print(f"Credentials file: {creds_file}")

        print("\n2. Setting up Google Sheets connection...")
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)

        print("\n3. Attempting to open spreadsheet...")
        sheet = client.open_by_key(sheet_id).sheet1
        
        print("\n4. Reading spreadsheet data...")
        headers = sheet.row_values(1)  # Get headers
        print(f"Headers found: {headers}")
        
        print("\n✅ Connection test successful!")
        return True

    except FileNotFoundError as e:
        print(f"\n❌ Error: Credentials file not found: {str(e)}")
        return False
    except gspread.exceptions.APIError as e:
        print(f"\n❌ Error: Google Sheets API error: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Google Sheets Connection...\n")
    test_connection() 