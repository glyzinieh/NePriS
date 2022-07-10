import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import dirname, join
from time import time

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


smtpobj = smtplib.SMTP('smtp.gmail.com',587)
smtpobj.starttls()
smtpobj.login(os.environ['GMAIL_ACCOUNT'],os.environ['GMAIL_PASS'])

msg = MIMEText('test')
msg['Subject'] = 'NePriSからメール送信のテスト'
msg['From'] = os.environ['GMAIL_ACCOUNT']
msg['To'] = 'glyzinie.h@gmail.com'
msg['Date'] = formatdate()

smtpobj.send_message(msg)
smtpobj.close()
