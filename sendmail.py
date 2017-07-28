# -*- coding: utf-8 -*
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import config
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendmail(content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(config.from_addr)
    msg['To'] = _format_addr(config.to_addr)
    msg['Subject'] = Header('hello, send by Python...', 'utf-8').encode()

    server = smtplib.SMTP_SSL('smtp.qq.com',465)
    # server.set_debuglevel(1)
    server.login(config.from_addr,config.password)
    server.sendmail(config.from_addr,config.to_addr, msg.as_string())
    server.quit()


