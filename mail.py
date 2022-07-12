import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


class gmail:
    def __init__(self, address: str, password: str) -> None:
        self.address = address
        self.smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtpobj.starttls()
        self.smtpobj.login(address, password)

    def creat(self, Subject: str, Body: str, To: str) -> MIMEText:
        msg = MIMEText(Body)
        msg['Subject'] = Subject
        msg['From'] = self.address
        msg['To'] = To
        msg['Date'] = formatdate()
        return msg

    def send(self, msg: MIMEText):
        return self.smtpobj.send_message(msg)

    def __del__(self):
        self.smtpobj.close()
