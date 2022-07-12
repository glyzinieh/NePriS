import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


class gmail:
    def __init__(self, address: str, password: str) -> None:
        self.address = address
        self.password = password

    def creat(self, Subject: str, Body: str, To: str) -> MIMEText:
        msg = MIMEText(Body)
        msg['Subject'] = Subject
        msg['From'] = self.address
        msg['To'] = To
        msg['Date'] = formatdate()
        return msg

    def send(self, msg: MIMEText):
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.starttls()
        smtpobj.login(self.address, self.password)
        return smtpobj.send_message(msg)

    def __del__(self):
        self.smtpobj.close()
