import gspread
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
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
worksheet = sheet.worksheet('Book Category')

def add_category(details):
    values = [
        details.get('row_num'),
        details.get('cat_id'),
        details.get('cat_name'),
        details.get('description'),
        details.get('book_names'),
        details.get('status')
    ]
    worksheet.append_row(values, value_input_option='USER_ENTERED')

category_details = {
    'row_num': '=ROW()',
    'cat_id': 'CAT_1',
    'cat_name': 'Science Fiction',
    'description': 'Futuristic and imaginative science-based stories',
    'book_names': 'Dune, Neuromancer, Snow Crash',
    'status': 0
}

print(add_category(category_details))

update_detail = {
    'row_num': '=ROW()',
    'cat_id': 'CAT_1',
    'cat_name': 'Science Fiction',
    'description': 'Futuristic and imaginative science-based stories',
    'book_names': 'Dune, Neuromancer, Snow Crash',
    'status': 0
}

def update_category(row_num, details):
    values = [[
        details.get('row_num'),
        details.get('cat_id'),
        details.get('cat_name'),
        details.get('description'),
        details.get('book_names'),
        details.get('status')
    ]]
    worksheet.update(values, f'A{row_num}:E{row_num}', value_input_option='USER_ENTERED')

update_category(2, update_detail)    

def get_category_by_row_num(row_num):
    row_values = worksheet.get(f'A{row_num}:E{row_num}')
    print(row_values)

get_category_by_row_num(2)

def get_all_categories():
    all_values = worksheet.get_all_values()
    print(all_values)

get_all_categories()

def get_books_by_category(cat_name):
    all_values = worksheet.get_all_values()
    cat_id = [row[1] for row in all_values[1:] if row[2] == cat_name]
    if cat_id:
        books = [row[4] for row in all_values[1:] if row[2] == cat_name]
        print(f'{cat_name}: {books}')
        return books
    else:
        print(f'Category {cat_name} not found')
        return []

get_books_by_category('Science Fiction')

def delete_category(row_num):
    delete_value = worksheet.update_acell(f'F{row_num}', 1)
    print(delete_value)
delete_category(2)