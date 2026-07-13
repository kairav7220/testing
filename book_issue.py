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
worksheet = sheet.worksheet('Book Issue')

def book_issue(details):
    row_num = f'=ROW()'
    timestamp = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')
    transaction_id = f'TXN_1'
    values = [
        row_num,
        details.get('transaction_id'),
        details.get('transaction_date'),
        timestamp,
        details.get('book_id'),
        details.get('issued_date'),
        details.get('mem_id'),
        details.get('recieved_by'),
        details.get('recieved_date')
    ]
    worksheet.append_row(values, value_input_option='USER_ENTERED')

issue_details = {
    'transaction_date': '25-Jan-2026',
    'book_id': 'BOOK_1',
    'issued_date': '25-Jan-2026',
    'mem_id': 'MEM_1',
    'recieved_by': '',
    'recieved_date': ''
}

print(book_issue(issue_details))

return_details = {
    'recieved_by': 'EMP_1',
    'recieved_date': '26-Feb-2026'
}

def book_return(row_num, details):
    issue_details = worksheet
    values = [[
        details.get('recieved_by'),
        details.get('recieved_date')
    ]]
    worksheet.update(values, f'H{row_num}:I{row_num}', value_input_option='USER_ENTERED')

print(book_return(2, return_details))

def get_issue_return_by_row(row_num):
    row_values = worksheet.get(f'A{row_num}:I{row_num}')
    print(row_values)
get_issue_return_by_row(2)

def get_all_issues_returns():
    all_values = worksheet.get_all_values()
    print(all_values)

get_all_issues_returns()