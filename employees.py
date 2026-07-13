import gspread
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
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
worksheet = sheet.worksheet('Employee Table')

def add_employee(details):
    values = [
        details.get('row_num'),
        details.get('emp_id'),
        details.get('name'),
        details.get('user_id'),
        details.get('password'),
        details.get('email'),
        details.get('phone'),
        details.get('designation'),
        details.get('salary'),
        details.get('user_row_num'),
        details.get('permanent_address'),
        details.get('temporary_address'),
        details.get('status')
    ]
    print(f'details: {values}')

    worksheet.append_row(values, value_input_option='USER_ENTERED')

# detail storing a value in a member
member_detail = {
    'row_num': '=ROW()',
    'emp_id': 'EMP_1',
    'name': 'raju',
    'user_id': 'USER_6',
    'password': 'emp123',
    'email': 'emp@test.com',
    'designation': 'librarian',
    'phone': 9876543210,
    'salary': 10000,
    'user_row_num': 2,
    'permanent_address': 'werw',
    'temporary_address': 'rtw',
    'status': 0
}

member = add_employee(member_detail)
print(member)

update_detail = {
    'row_num': '=ROW()',
    'emp_id': 'EMP_1',
    'name': 'rajesh',
    'user_id': 'USER_6',
    'password': 'emp21312',
    'email': 'emp@library.com',
    'designation': 'librarian',
    'phone': 9876543210,
    'salary': 10000,
    'user_row_num': 2,
    'permanent_address': 'sdfs',
    'temporary_address': 'sdsd'
}

def update_employee(row_num, details):
    values = [[
        details.get('row_num'),
        details.get('emp_id'),
        details.get('name'),
        details.get('user_id'),
        details.get('password'),
        details.get('email'),
        details.get('phone'),
        details.get('designation'),
        details.get('salary'),
        details.get('user_row_num'),
        details.get('permanent_address'),
        details.get('temporary_address')
    ]]
    worksheet.update(values, 'A2:M2', value_input_option='USER_ENTERED')

update_employee(2, update_detail)

def get_employee_by_row_num(row_num):
    row_values = worksheet.get(f'A{row_num}:M{row_num}')
    print(row_values)

get_employee_by_row_num(3)

def get_all_employees():
    all_values = worksheet.get_all_values()
    print(all_values)

get_all_employees()

def delete_members(row_num):
    delete_value = worksheet.update_acell(f'M{row_num}', 1)
    print(delete_value)
delete_members(2)