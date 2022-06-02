import os
from os.path import dirname, join

import client
import gspread
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory
from flask_sitemap import Sitemap
from google.oauth2.service_account import Credentials
from werkzeug.utils import secure_filename

# ローカル環境で環境編集を取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Googleスプレッドシートからデータベースを取得
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

credential = {
    "type": "service_account",
    "project_id": os.environ['SHEET_PROJECT_ID'],
    "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
    "private_key": os.environ['SHEET_PRIVATE_KEY'].replace('\\n', '\n'),
    "client_email": os.environ['SHEET_CLIENT_EMAIL'],
    "client_id": os.environ['SHEET_CLIENT_ID'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
    }
credentials = Credentials.from_service_account_info(credential,scopes=scope)
# ログイン
gc = gspread.authorize(credentials)
# シートを開く
wb = gc.open_by_key(os.environ['SHEET_DATABASE_KEY'])
ws = wb.worksheet("Main")

file_send = client.file_send(os.environ['DB_URL'],os.environ['DB_TOKEN'])

app = Flask(__name__)
ext = Sitemap(app=app)

ALLOWED_EXTENSIONS = {'png','jfif','pjpeg','jpeg','pjp','jpg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
def index():
    return render_template('index.html')
@ext.register_generator
def index():
    yield 'index', {}

@app.get('/about/')
def about():
    return render_template('about.html')
@ext.register_generator
def about():
    yield 'about', {}

@app.get('/contact/')
def contact():
    return render_template('contact.html')
@ext.register_generator
def contact():
    yield 'contact', {}

@app.get('/record/')
def record():
    return render_template('record.html')
@ext.register_generator
def record():
    yield 'record', {}

@app.post('/record/thanks/')
def record_thanks():
    # fileがない場合
    if 'image' not in request.files:
        return render_template(
            'record_thanks.html',
            status='登録できませんでした。ファイルを送信してください。'
            )
    file = request.files['image']

    # filenameが空の場合
    if file.filename == '':
        return render_template(
            'record_thanks.html',
            status='登録できませんでした。ファイルの名前を指定してください。'
            )

    if file and allowed_file(file.filename):
        fileext = os.path.splitext(secure_filename(file.filename))[1]
    else:
        return render_template(
            'record_thanks.html',
            status='登録できませんでした。PNG,JPEGのみ送信できます。'
            )
 
    id = str(int(ws.col_values(1)[-1])+1).zfill(5)
    filename = id + fileext
    answer = request.form
    save_data = [
        id,
        answer['email'],
        answer['name'],
        answer['title'],
        filename,
        answer['date'],
        answer.get('note',''),
        answer.get('no_seven',''),
        answer.get('no_family','')
    ]
    
    ws.append_row(save_data)
    file_send.write(filename,file)
    return render_template(
            'record_thanks.html',
            status='ご登録ありがとうございます。'
            )

@app.get('/privacy-policy/')
def privacy():
    return render_template('privacy-policy.html')
@ext.register_generator
def privacy():
    yield 'privacy', {}

@app.get('/temp/<path:path>/')
def send_temp(path):
    return send_from_directory('temp', path)

if __name__ == "__main__":
    app.run(port=8000,debug=True)
