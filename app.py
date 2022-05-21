import os
from os.path import dirname, join

import client
import gspread
import requests
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sitemap import Sitemap
from google.oauth2.service_account import Credentials

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

# データベースのシートを開く
database_sheet = gc.open_by_key(os.environ['SHEET_DATABASE_KEY'])

http_data = client.file_send(os.environ['DB_URL'],os.environ['DB_TOKEN'])

app = Flask(__name__)
ext = Sitemap(app=app)

@app.route('/')
def index():
    return render_template('index.html')
@ext.register_generator
def index():
    yield 'index', {}

@app.route('/about/')
def about():
    return render_template('about.html')
@ext.register_generator
def about():
    yield 'about', {}

@app.route('/contact/')
def contact():
    return render_template('contact.html')
@ext.register_generator
def contact():
    yield 'contact', {}

@app.route('/contact/thanks/')
def contact_thanks():
    return render_template('contact_thanks.html')

@app.route('/record/')
def record():
    return render_template('record.html')
@ext.register_generator
def record():
    yield 'record', {}

@app.route('/record/thanks/', methods=['POST'])
def record_thanks():
    return render_template('record_thanks.html')

if __name__ == "__main__":
    app.run(port=8000,debug=True)
