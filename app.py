import os
from os.path import dirname, join

import gspread
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory
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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/favicon.ico/')
def favicon():
    return send_from_directory('/favicon.ico/')

if __name__ == "__main__":
    app.run(port=8000,debug=True)
