# -*- coding: gbk -*-
from flask import Flask, abort, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import base.Log as log
import time

app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

config = {}
config.setdefault('mail_host', "smtp.sina.com")
config.setdefault('mail_port', 25)
config.setdefault('mail_user', "jacklaiu@sina.com")
config.setdefault('mail_pass', "queue11235813")
config.setdefault('sender', "jacklaiu@sina.com")

def send(subject=None, content=None, receivers='jacklaiu@qq.com', contenttype="plain"):

    receivers = [receivers] if receivers.index('@') == -1 else receivers.split('@@')  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, contenttype, 'utf-8')
    message['From'] = "{}".format(config['sender'])
    message['To'] = ",".join(receivers)

    message['Subject'] = Header(subject, 'utf-8')

    error_msg = None
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(config['mail_host'], config['mail_port'])
        smtpObj.login(config['mail_user'], config['mail_pass'])
        smtpObj.sendmail(config['sender'], receivers, message.as_string())
        log.log("邮件发送成功")
    except Exception as e:
        time.sleep(5)
        config.setdefault('mail_host', "smtp.qq.com")
        config.setdefault('mail_port', 25)
        config.setdefault('mail_user', "jacklaiu@foxmail.com")
        config.setdefault('mail_pass', "wesmpmzsdcsebfic")
        config.setdefault('sender', "jacklaiu@foxmail.com")
        log.log("正在重发")
        send(subject=subject, content=content, receivers=receivers, contenttype=contenttype)
    return "OK" if error_msg is None else error_msg

@app.route('/smtpclient/sendPlain/<subject>/<content>/<receivers>')
def sendPlain(subject=None, content=None, receivers='jacklaiu@qq.com'):
    send(subject, content, receivers, 'plain')
    return "OK"

@app.route('/smtpclient/sendHtml/<subject>/<content>/<receivers>')
def sendHtml(subject=None, content=None, receivers='jacklaiu@qq.com'):
    send(subject, content, receivers, 'html')
    return "OK"

app.run(host="0.0.0.0", port=64210)

