import datetime
import os
import re
import time
from io import BytesIO
from os.path import dirname, join

import client
import gspread
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_file
from flask_sitemap import Sitemap
from google.oauth2.service_account import Credentials
from PIL import Image
from werkzeug.datastructures import FileStorage

import gspread_mod

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
main_sheet = wb.worksheet("Main")
logs_sheet = wb.worksheet("Logs")

file_send = client.file_send(os.environ['DB_URL'], os.environ['DB_TOKEN'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
ext = Sitemap(app=app)

@app.before_request
def before_request():
    if not request.is_secure and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


def allowed_image(file: FileStorage):
    return '.' in file.filename and \
           re.match('image/.+', file.mimetype)


@app.get('/')
def index():
    data = main_sheet.get_all_dicts()[-50:]
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

    id = str(int(max(main_sheet.col_values(1)[1:],key=int))+1).zfill(5)

    filename = id + '.webp'

    answer = request.form.to_dict()
    if answer['no_seven'] == '':
        answer['no_seven'] = '登録されていません'
    if answer['no_family'] == '':
        answer['no_family'] = '登録されていません'
    save_data = [
        id,
        answer['email'],
        answer['name'],
        answer['title'],
        filename,
        answer['date'],
        answer['note'],
        answer['no_seven'],
        answer['no_family']
    ]
    main_sheet.append_row(save_data)

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


@app.get('/tos/')
def tos():
    return render_template('tos.html')


@ext.register_generator
def privacy():
    yield 'tos', {}


@app.get('/work/<string:id>/')
def work(id):
    db = main_sheet.get_all_dicts()
    detail = next(i for i in db if i['id'] == id)
    return render_template('work.html', result=detail)


@app.get('/img/<string:filename>/')
def get_img(filename):
    file = BytesIO()
    file.write(file_send.read(filename).content)
    file.seek(0)
    return send_file(file, attachment_filename=filename)


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    if error.code == 404:
        msg = 'ページが見つかりませんでした。'
    else:
        msg = str()

    dt = str(datetime.datetime.fromtimestamp(time.time()))
    log = [
        dt,
        error.code,
        error.name,
        request.remote_addr,
        request.path,
        request.user_agent.string
    ]
    logs_sheet.append_row(log)
    return render_template('error.html', error=error, msg=msg),error.code


if __name__ == "__main__":
    app.run(port=8000, debug=True)
