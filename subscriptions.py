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
credentials = Credentials.from_service_account_file("credentials.json", scopes=scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
worksheet = sheet.worksheet('Subscription Table')

def add_plan(details):
    values = [
        details.get('row_num'),
        details.get('transaction_id'),
        details.get('transaction_date'),
        details.get('timestamp'),
        details.get('transaction_mode'),
        details.get('mem_id'),
        details.get('mem_subscription_amount'),
        details.get('plan_type'),
        details.get('plan_start'),
        details.get('plan_end'),
        details.get('subscription_status')
    ]
    print(f'details: {values}')
    worksheet.append_row(values, value_input_option='USER_ENTERED')

subscription_detail = {
    'row_num': '=ROW()',
    'transaction_id': 'TXN_1',
    'transaction_date': '22-Jan-2026',
    'timestamp': datetime.now().strftime("%I:%M:%S %p"),
    'transaction_mode': 'online',
    'mem_id': 'MEM_1',
    'mem_subscription_amount': 200,
    'plan_type': 'Annual',
    'plan_start': '22-Jan-2026',
    'plan_end': '21-Jan-2027',
    'subscription_status': 0
}

print(add_plan(subscription_detail))

update_detail = {
    'row_num': '=ROW()',
    'transaction_id': 'TXN_1',
    'transaction_date': '20-Jan-2026',
    'timestamp': datetime.now().strftime("%I:%M:%S %p"),
    'transaction_mode': 'online',
    'mem_id': 'MEM_1',
    'mem_subscription_amount': 300,
    'plan_type': 'Annual',
    'plan_start': '22-Jan-2026',
    'plan_end': '21-Jan-2027',
    'subscription_status': 0
}

def update_plan(row_num, details):
    values = [[
        details.get('row_num'),
        details.get('transaction_id'),
        details.get('transaction_date'),
        details.get('timestamp'),
        details.get('transaction_mode'),
        details.get('mem_id'),
        details.get('mem_subscription_amount'),
        details.get('plan_type'),
        details.get('plan_start'),
        details.get('plan_end'),
        details.get('subscription_status')
    ]]
    worksheet.update(values, 'A2:J2', value_input_option='USER_ENTERED')

update_plan(2, update_detail)

def get_subscription_by_row_num(row_num):
    row_values = worksheet.get(f'A{row_num}:J{row_num}')
    print(row_values)

get_subscription_by_row_num(3)

def get_all_subscriptions():
    all_values = worksheet.get_all_values()
    print(all_values)

get_all_subscriptions()

def delete_subscription(row_num):
    delete_value = worksheet.update_acell(f'J{row_num}', 1)
    print(delete_value)
delete_subscription(2)