import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import jsonify
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# Setup Google Sheets connection
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GOOGLE_CREDENTIALS_FILE'), scope)
client = gspread.authorize(creds)

# Open the spreadsheet
SHEET_ID = os.getenv('SHEET_ID')
sheet = client.open_by_key(SHEET_ID).sheet1

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, username, password, email, location):
    try:
        # Check if username or email already exists
        existing_users = sheet.get_all_records()
        for user in existing_users:
            if user['Username'] == username:
                return {"error": "Username already exists"}, 400
            if user['Email'] == email:
                return {"error": "Email already exists"}, 400
        
        # Hash the password
        hashed_password = hash_password(password)
        
        # Add new user
        sheet.append_row([name, username, hashed_password, email, location])
        return {"message": "Registration successful"}, 200
    
    except Exception as e:
        return {"error": str(e)}, 500

def login_user(username, password):
    try:
        users = sheet.get_all_records()
        hashed_password = hash_password(password)
        
        for user in users:
            if user['Username'] == username and user['Password'] == hashed_password:
                return {
                    "message": "Login successful",
                    "user": {
                        "name": user['Name'],
                        "username": user['Username'],
                        "email": user['Email'],
                        "location": user['Location']
                    }
                }, 200
        
        return {"error": "Invalid username or password"}, 401
    
    except Exception as e:
        return {"error": str(e)}, 500 