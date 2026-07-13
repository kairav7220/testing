import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import random
import os

load_dotenv()

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets'
]

credentials = Credentials.from_service_account_file(os.getenv("GOOGLE_SHEETS_CREDS_PATH"), scopes=scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
worksheet = sheet.worksheet('Customer Table')

def add_customer():
    try:
        CustID = input('Enter Customer ID: ')
        Name = input('Enter Name: ')
        Username = input('Enter Username: ')
        Password = input('Enter Password: ')
        worksheet.append_row([CustID, Name, Username, Password])
        print('Customer added successfully!')
    except Exception as e:
        print(f'Error adding customer: {e}')

add_customer()