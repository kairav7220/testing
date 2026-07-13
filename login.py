import gspread
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
print(os.getenv('GOOGLE_SHEET_ID'))

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets'
]

# Replace os.getenv("GOOGLE_CREDENTIALS") with the actual filename string
credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
gc = gspread.authorize(credentials)

# Open the subscriptions sheet
sheet = gc.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
worksheet = sheet.worksheet('Logs')
users_table = sheet.worksheet('User Table')

def login(username, password):
    all_values = users_table.get_all_values()
    for i in all_values[1:]:
        if username == i[3] and password == i[4]:
            print('Successful Login!')
            values = [
                '=ROW()',
                datetime.now().strftime('%d-%m-%Y %I:%M:%S %p'),
                f'{username} has logged in'
            ]
            worksheet.append_row(values, value_input_option='USER_ENTERED')

print(login('user1', 'user123'))

def logout(username):
    values = [
        '=ROW()',
        datetime.now().strftime('%d-%m-%Y %I:%M:%S %p'),
        f'{username} has logged out'
    ]
            
    worksheet.append_row(values, value_input_option='USER_ENTERED')

print(logout('user1'))