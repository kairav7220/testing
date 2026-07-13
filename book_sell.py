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
worksheet = sheet.worksheet('Book Sell')

def book_order(details):
    row_num = f'=ROW()'
    timestamp = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')
    order_id = f'ORDER_1'
    values = [
        row_num,
        order_id,
        details.get('order_date'),
        timestamp,
        details.get('book_id'),
        details.get('book_name'),
        details.get('book_price'),
        details.get('mem_id'),
    ]
    worksheet.append_row(values, value_input_option='USER_ENTERED')

order_details = {
    'order_date': '25-Jan-2026',
    'book_id': 'BOOK_1',
    'book_name': 'Duke',
    'book_price': 200,
    'mem_id': 'MEM_1'
}

print(book_order(order_details))

update_detail = {
    'order_date': '25-Jan-2026',
    'timestamp': datetime.now().strftime('%d-%m-%Y %I:%M:%S %p'),
    'book_id': 'BOOK_2',
    'book_name': 'Neuromancer',
    'book_price': 210,
    'mem_id': 'MEM_2'
}

def order_book(row_num, details):
    issue_details = worksheet
    values = [[
        details.get('row_num'),
        details.get('order_id'),
        details.get('order_date'),
        details.get('timestamp'),
        details.get('book_id'),
        details.get('book_name'),
        details.get('book_price'),
        details.get('mem_id'),
    ]]
    worksheet.update(values, f'A{row_num}:H{row_num}', value_input_option='USER_ENTERED')
order_book(2, update_detail)