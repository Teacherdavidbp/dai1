import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

def setup_sheet():
    print("Setting up Google Sheet...")
    
    # Load credentials
    load_dotenv()
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GOOGLE_CREDENTIALS_FILE'), scope)
    client = gspread.authorize(creds)
    
    # Open sheet
    sheet = client.open_by_key(os.getenv('SHEET_ID')).sheet1
    
    # Clear existing content
    sheet.clear()
    
    # Set headers
    headers = ['Name', 'Username', 'Password', 'Email', 'Location']
    sheet.insert_row(headers, 1)
    
    print("Sheet setup complete!")
    print(f"Headers added: {headers}")

if __name__ == "__main__":
    setup_sheet()