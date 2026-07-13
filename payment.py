import gspread
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime
from gspread.utils import rowcol_to_a1
import random
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
worksheet = sheet.worksheet('Payment Table')

def add_payment(details):
    values = [
        details.get('row_num'),
        details.get('transaction_id'),
        details.get('transaction_date'),
        details.get('timestamp'),
        details.get('payment_amount'),
        details.get('payment_type'),
        details.get('payment_mode'),
        details.get('payment_status'),
        details.get('paid_by'),
        details.get('recieved_by'),
        details.get('user_row_num')
    ]
    worksheet.append_row(values, value_input_option='USER_ENTERED')

paymen_details = {
    'row_num': '=ROW()',
    'transaction_id': 'TXN_1',
    'transaction_date': '22-Jan-2026',
    'timestamp': datetime.now().strftime('%I:%M:%S %p'),
    'payment_amount': 200,
    'payment_type': 'Subscription',
    'payment_mode': 'Cash',
    'payment_status': 'Accepted',
    'paid_by': 'MEM_1',
    'recieved_by': 'EMP_1',
    'user_row_num': 2
}
print(add_payment(paymen_details))

def get_payment_by_row_num(row_num):
    row_values = worksheet.get(f'A{row_num}:K{row_num}')
    print(row_values)

get_payment_by_row_num(2)

def get_all_payments():
    all_values = worksheet.get_all_values()
    print(all_values)

get_all_payments()