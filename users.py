import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import random
import os

load_dotenv()

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(os.getenv('GOOGLE_SHEETS_CREDS_PATH'), scopes=scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
worksheet = sheet.worksheet('User Table')

# Adds a new user to the sheet with auto-generated row number and user ID
def add_user(user_data):
    all_values = worksheet.get_all_values()
    next_row = len(all_values) + 1
    # Combines auto-generated row number formula and user ID formula with the user data passed in
    row_data = [f'=ROW()', f'="USER_"&A{next_row}-1'] + user_data
    worksheet.update([row_data], f'A{next_row}:H{next_row}', value_input_option='USER_ENTERED')
    print(f'User added at row {next_row}')

# Searches for a user by their user ID and returns their row number
def get_user_by_row(user_id):
    all_values = worksheet.get_all_values()
    # Loops through each row in the sheet (skipping header), keeps only rows where status column (H) equals 0 meaning active
    active_users = [row for row in all_values[1:] if int(row[7]) == 0]
    # enumerate gives index (i) and value (row) together, loops through active users to find matching user_id
    for i, row in enumerate(active_users):
        if row[1] == user_id:
            return i + 2
    return None

# Returns all active users from the sheet
def get_all_users():
    all_values = worksheet.get_all_values()
    # Loops through each row in the sheet (skipping header), keeps only rows where status column (H) equals 0 meaning active
    active_users = [row for row in all_values[1:] if int(row[7]) == 0]
    for user in active_users:
        print(user)
    return active_users

# Soft deletes a user by setting status to 1 in column H
def delete_users(row_num):
    worksheet.update_acell(f'H{row_num}', 1)
    print(f'User at row {row_num} deleted')

user1 = ['member', 'john', 'pass123', 'john@test.com', 9876543210, 0]
user2 = ['employee', 'jane', 'pass456', 'jane@test.com', 9876543211, 0]

# Calls
add_user(user1)
add_user(user2)
get_all_users()
delete_users(3)