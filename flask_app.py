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
worksheet = sheet.worksheet('User Table')

app = Flask(__name__)

@app.route('/')
def index():
    all_values = worksheet.get_all_values()
    headers = all_values[0]
    rows = []
    for i, row in enumerate(all_values[1:], start=2):
        if row[7] == '0':
            rows.append({'data': row, 'sheet_row': i})
    return render_template('index.html', headers=headers, rows=rows)

@app.route('/list')
def get_all_users():
    all_values = worksheet.get_all_values()
    return jsonify({'sheet_data': all_values})

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        all_values = worksheet.get_all_values()
        next_row = len(all_values) + 1
        worksheet.update_acell(f'C{next_row}', user_type)
        worksheet.update_acell(f'D{next_row}', username)
        worksheet.update_acell(f'E{next_row}', password)
        worksheet.update_acell(f'G{next_row}', phone)
        worksheet.update_acell(f'H{next_row}', '0')
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/update/<int:row_num>', methods=['GET', 'POST'])
def update_user(row_num):
    if request.method == 'POST':
        password = request.form.get('password')
        phone = request.form.get('phone')
        worksheet.update_acell(f'E{row_num}', password)
        worksheet.update_acell(f'G{row_num}', phone)
        return redirect(url_for('index'))

    user_row = worksheet.get(f'A{row_num}:J{row_num}')[0]
    return render_template('form.html', user=user_row, row_num=row_num)

@app.route('/delete/<int:row_num>')
def delete_user(row_num):
    worksheet.update_acell(f'H{row_num}', '1')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
