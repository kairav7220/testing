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

credentials = Credentials.from_service_account_file(os.getenv('GOOGLE_SHEETS_CREDS_PATH'), scopes=scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
worksheet = sheet.worksheet('Member Table')

def add_member(details):
    row_num = f'=ROW()'
    mem_id = f'USER_1'
    # get all columns from member details
    values = [
        row_num,
        mem_id,
        details.get('name'),
        details.get('user_id'),
        details.get('password'),
        details.get('email'),
        details.get('phone'),
        details.get('user_row_num'),
        details.get('permanent_address'),
        details.get('temporary_address'),
        details.get('status')
    ]
    print(f'details: {values}')

    worksheet.append_row(values, value_input_option='USER_ENTERED')

# detail storing a value in a member
member_detail = {
    'name': 'ajay',
    'user_id': 'USER_1',
    'password': 'user123',
    'email': 'user@test.com',
    'phone': 9876543210,
    'user_row_num': 2,
    'permanent_address': 'abc',
    'temporary_address': 'abcd',
    'status': 0
}

# calling function with member detail
member = add_member(member_detail)
print(member)

update_detail = {
    'row_num': '=ROW()',
    'mem_id': 'MEM_1',
    'name': 'raju',
    'user_id': 'USER_1',
    'password': 'user16658',
    'email': 'user@test.com',
    'phone': 1234567890,
    'user_row_num': 2,
    'permanent_address': 'abc',
    'temporary_address': 'dffh',
    'status': 0
}

def update_member(row_num, details):
    values = [[
        details.get('row_num'),
        details.get('mem_id'),
        details.get('name'),
        details.get('user_id'),
        details.get('password'),
        details.get('email'),
        details.get('phone'),
        details.get('user_row_num'),
        details.get('permanent_address'),
        details.get('temporary_address')
    ]]
    worksheet.update(values, 'A3:J3', value_input_option='USER_ENTERED')

update_member(3, update_detail)

def get_members_by_row_num(row_num):
    row_values = worksheet.get(f'A{row_num}:J{row_num}')
    print(row_values)

get_members_by_row_num(2)

def get_all_members():
    all_values = worksheet.get_all_values()
    print(all_values)

get_all_members()

def delete_members(row_num):
    delete_value = worksheet.update_acell(f'K{row_num}', 1)
    print(delete_value)
delete_members(4)