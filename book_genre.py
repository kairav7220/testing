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
worksheet = sheet.worksheet('Book Genre')

def add_book(details):
    values = [
        details.get('row_num'),
        details.get('genre_id'),
        details.get('genre_title'),
        details.get('book_names'),
        details.get('status')
    ]
    worksheet.append_row(values, value_input_option='USER_ENTERED')

book_details = {
    'row_num': '=ROW()',
    'genre_id': 'GENRE_1',
    'genre_title': 'Science Fiction',
    'book_names': 'Dune, Neuromancer, Foundation',
    'status': 0
}

print(add_book(book_details))

update_detail = {
    'row_num': '=ROW()',
    'genre_id': 'GENRE_1',
    'genre_title': 'Fantasy',
    'book_names': 'The Hobbit, Harry Potter, Game of Thrones',
    'status': 0
}

def update_book(row_num, details):
    values = [[
        details.get('row_num'),
        details.get('genre_id'),
        details.get('genre_title'),
        details.get('book_names'),
        details.get('status')
    ]]
    worksheet.update(values, f'A{row_num}:E{row_num}', value_input_option='USER_ENTERED')

update_book(2, update_detail)

def get_book_by_row_num(row_num):
    row_values = worksheet.get(f'A{row_num}:E{row_num}')
    print(row_values)
get_book_by_row_num(2)

def get_all_books():
    all_values = worksheet.get_all_values()
    print(all_values)

get_all_books()

def delete_book(row_num):
    delete_value = worksheet.update_acell(f'E{row_num}', 1)
    print(delete_value)
delete_book(2)