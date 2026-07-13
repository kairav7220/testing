from flask import Flask, jsonify, render_template, request, redirect, url_for
import gspread
import os
import json
from google.oauth2.service_account import Credentials

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets'
]

creds_json = os.environ.get('GOOGLE_CREDENTIALS')
if creds_json:
    creds_dict = json.loads(creds_json)
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
else:
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)

gc = gspread.authorize(credentials)

sheet = gc.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
user_worksheet = sheet.worksheet('User Table')
book_worksheet = sheet.worksheet('Book Table')
member_worksheet = sheet.worksheet('Member Table')

app = Flask(__name__)

# ─── Users ───────────────────────────────────────────────

@app.route('/')
def index():
    all_values = user_worksheet.get_all_values()
    headers = all_values[0]
    rows = []
    for i, row in enumerate(all_values[1:], start=2):
        if row[7] == '0':
            rows.append({'data': row, 'sheet_row': i})
    return render_template('index.html', headers=headers, rows=rows)

@app.route('/list')
def get_all_users():
    all_values = user_worksheet.get_all_values()
    return jsonify({'sheet_data': all_values})

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        all_values = user_worksheet.get_all_values()
        next_row = len(all_values) + 1
        row_data = ['=ROW()', f'="USER_"&A{next_row}-1', user_type, username, password, email, phone, '0']
        user_worksheet.update([row_data], f'A{next_row}:H{next_row}', value_input_option='USER_ENTERED')
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/update/<int:row_num>', methods=['GET', 'POST'])
def update_user(row_num):
    if request.method == 'POST':
        password = request.form.get('password')
        phone = request.form.get('phone')
        user_worksheet.update_acell(f'E{row_num}', password)
        user_worksheet.update_acell(f'G{row_num}', phone)
        return redirect(url_for('index'))

    user_row = user_worksheet.get(f'A{row_num}:J{row_num}')[0]
    return render_template('form.html', user=user_row, row_num=row_num)

@app.route('/delete/<int:row_num>')
def delete_user(row_num):
    user_worksheet.update_acell(f'H{row_num}', '1')
    return redirect(url_for('index'))

# ─── Books ───────────────────────────────────────────────

@app.route('/books')
def books():
    all_values = book_worksheet.get_all_values()
    headers = all_values[0]
    rows = []
    for i, row in enumerate(all_values[1:], start=2):
        if row[9] == '0':
            rows.append({'data': row, 'sheet_row': i})
    return render_template('books.html', headers=headers, rows=rows)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        book_price = request.form.get('book_price')
        book_cat = request.form.get('book_cat')
        book_genre = request.form.get('book_genre')
        edition = request.form.get('edition')
        publication = request.form.get('publication')
        all_values = book_worksheet.get_all_values()
        next_row = len(all_values) + 1
        row_data = ['=ROW()', f'="BOOK_"&A{next_row}-1', book_name, book_author, book_price, book_cat, book_genre, edition, publication, '0']
        book_worksheet.update([row_data], f'A{next_row}:J{next_row}', value_input_option='USER_ENTERED')
        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/books/edit/<int:row_num>', methods=['GET', 'POST'])
def edit_book(row_num):
    if request.method == 'POST':
        book_worksheet.update_acell(f'C{row_num}', request.form.get('book_name'))
        book_worksheet.update_acell(f'D{row_num}', request.form.get('book_author'))
        book_worksheet.update_acell(f'E{row_num}', request.form.get('book_price'))
        book_worksheet.update_acell(f'F{row_num}', request.form.get('book_cat'))
        book_worksheet.update_acell(f'G{row_num}', request.form.get('book_genre'))
        book_worksheet.update_acell(f'H{row_num}', request.form.get('edition'))
        book_worksheet.update_acell(f'I{row_num}', request.form.get('publication'))
        return redirect(url_for('books'))

    book_row = book_worksheet.get(f'A{row_num}:J{row_num}')[0]
    return render_template('edit_book.html', book=book_row, row_num=row_num)

@app.route('/books/delete/<int:row_num>')
def delete_book(row_num):
    book_worksheet.update_acell(f'J{row_num}', '1')
    return redirect(url_for('books'))

# ─── Members ───────────────────────────────────────────────

@app.route('/members')
def members():
    all_values = member_worksheet.get_all_values()
    headers = all_values[0]
    rows = []
    for i, row in enumerate(all_values[1:], start=2):
        if row[10] == '0':
            rows.append({'data': row, 'sheet_row': i})
    return render_template('members.html', headers=headers, rows=rows)

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        permanent_address = request.form.get('permanent_address')
        temporary_address = request.form.get('temporary_address')
        all_values = member_worksheet.get_all_values()
        next_row = len(all_values) + 1
        row_data = ['=ROW()', f'="MEM_"&A{next_row}-1', name, user_id, password, email, phone, '', permanent_address, temporary_address, '0']
        member_worksheet.update([row_data], f'A{next_row}:K{next_row}', value_input_option='USER_ENTERED')
        return redirect(url_for('members'))
    return render_template('add_member.html')

@app.route('/members/edit/<int:row_num>', methods=['GET', 'POST'])
def edit_member(row_num):
    if request.method == 'POST':
        member_worksheet.update_acell(f'C{row_num}', request.form.get('name'))
        member_worksheet.update_acell(f'D{row_num}', request.form.get('user_id'))
        member_worksheet.update_acell(f'E{row_num}', request.form.get('password'))
        member_worksheet.update_acell(f'F{row_num}', request.form.get('email'))
        member_worksheet.update_acell(f'G{row_num}', request.form.get('phone'))
        member_worksheet.update_acell(f'I{row_num}', request.form.get('permanent_address'))
        member_worksheet.update_acell(f'J{row_num}', request.form.get('temporary_address'))
        return redirect(url_for('members'))

    member_row = member_worksheet.get(f'A{row_num}:K{row_num}')[0]
    return render_template('edit_member.html', member=member_row, row_num=row_num)

@app.route('/members/delete/<int:row_num>')
def delete_member(row_num):
    member_worksheet.update_acell(f'K{row_num}', '1')
    return redirect(url_for('members'))

if __name__ == '__main__':
    app.run(debug=True)