#!/usr/bin/env python3
# -*- coding:utf-8 -*

from DataCmp import DataCmp
import configparser
import lxml
import time
from lxml.html import builder as E
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL 

def mailgen():
    d = DataCmp().cmp_result()
    news_topic = {
        'hot_news' : '热点新闻',
        'hot_inform' : '最新公告',
        'hot_msg' : '最新简讯'
    }
    def test():
        for key, value in d.items():
            yield E.H2(news_topic[key])
            if any(value):
                for i in value:
                    yield lxml.html.fromstring(
                        '<a href="http://news.gdut.edu.cn/viewarticle.aspx?articleid={id}">{title}[{loc}]</a><br></br>'.format_map(i)
                    )
            else:
                del news_topic[key]
                yield E.P('无')
        yield E.P('Sent at {}'.format(time.strftime("%y-%m-%d %H:%M", time.localtime())))
    sub = [i for i in test()]
    if not any(news_topic):
        sub = [E.H2('今日无事可做')]
    html = E.HTML(
        E.HEAD(
            E.META(charset='UTF-8'),
            E.META(name='viewport', content='width=device-width, initial-scale=1.0'),
            E.TITLE("GDUTNews Stream")
        ),
        E.BODY(*sub)
    )
    return lxml.html.tostring(html)

def mailsend():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
    except FileNotFoundError:
        print('File Not Found')
    
    ###
    # USER CONFIG
    ###

    # server
    hostserver = config['SMTP']['hostserver']
    sender = config['SMTP']['sender']
    pwd = config['SMTP']['password']
    sendername = config['Profile']['sendername']
    receiverlist = config['Profile']['receiverlist'].split(',')
    #mail
    mail_content = mailgen()
    mail_title = 'GDUTNews邮件订阅'

    try:
        smtp = SMTP_SSL(hostserver)
        smtp.ehlo(hostserver)
        smtp.login(sender, pwd)
        msg = MIMEText(mail_content, 'html', 'UTF-8')
        msg['Subject'] = Header(mail_title, 'UTF-8')
        msg['From'] = sendername
        for receiver in receiverlist:
            msg["To"] = receiver
            smtp.sendmail(sendername, receiver, msg.as_string())
        smtp.close()
    except FileExistsError:
        print('error!')

if __name__ == "__main__":
    mailsend()