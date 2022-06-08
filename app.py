import os
import re
from io import BytesIO
from os.path import dirname, join

import client
import gspread
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from flask_sitemap import Sitemap
from google.oauth2.service_account import Credentials
from PIL import Image
from werkzeug.datastructures import FileStorage

# ローカル環境で環境編集を取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Googleスプレッドシートからデータベースを取得
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']

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
credentials = Credentials.from_service_account_info(credential, scopes=scope)
# ログイン
gc = gspread.authorize(credentials)
# シートを開く
wb = gc.open_by_key(os.environ['SHEET_DATABASE_KEY'])
ws = wb.worksheet("Main")

file_send = client.file_send(os.environ['DB_URL'], os.environ['DB_TOKEN'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
ext = Sitemap(app=app)


def allowed_image(file: FileStorage):
    return '.' in file.filename and \
           re.match('image/.+', file.mimetype)


def gspread_get_all_dict(ws: gspread.Worksheet) -> list[dict]:
    result = []
    data = ws.get_all_values()
    header = data[0]
    body = data[1:]
    for i in body:
        result.append(dict(zip(header, i)))
    return result


@app.get('/')
def index():
    data = gspread_get_all_dict(ws)[-50:]
    data.reverse()
    return render_template('index.html', data=data)


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
            status='Failed',
            msg='ファイルを送信してください。'
        )
    file = request.files['image']

    # filenameが空の場合
    if file.filename == '':
        return render_template(
            'record_thanks.html',
            status='Failed',
            msg='ファイルの名前を指定してください。'
        )

    if not (file and allowed_image(file)):
        return render_template(
            'record_thanks.html',
            status='Failed',
            msg='画像のみ送信できます。'
        )

    img_file = Image.open(file.stream).convert('RGB')
    img_save = BytesIO()
    img_file.save(img_save, 'webp')

    id = str(int(ws.col_values(1)[-1])+1).zfill(5)
    filename = id + '.webp'

    answer = request.form
    save_data = [
        id,
        answer['email'],
        answer['name'],
        answer['title'],
        filename,
        answer['date'],
        answer.get('note', ''),
        answer.get('no_seven', ''),
        answer.get('no_family', '')
    ]
    ws.append_row(save_data)

    file_send.write(filename, img_save.getvalue())
    return render_template(
        'record_thanks.html',
        status='Success',
        id=id
    )


@app.get('/howto-neppuri/')
def howto():
    return render_template('howto-neppuri.html')


@ext.register_generator
def howto():
    yield 'howto', {}


@app.get('/privacy-policy/')
def privacy():
    return render_template('privacy-policy.html')


@ext.register_generator
def privacy():
    yield 'privacy', {}


@app.get('/work/<string:id>/')
def work(id):
    db = gspread_get_all_dict(ws)
    detail = next(i for i in db if i['id'] == id)
    return render_template('work.html', result=detail)


@app.get('/img/<string:filename>/')
def get_img(filename):
    file = BytesIO()
    file.write(file_send.read(filename).content)
    file.seek(0)
    return send_file(file, attachment_filename=filename)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
