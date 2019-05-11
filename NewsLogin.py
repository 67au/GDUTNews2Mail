#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from lxml import etree
import re

class NewsLogin:

    URL_NEWS = 'http://news.gdut.edu.cn/default.aspx'
    URL_PRE = r'http:\/\/news.gdut\.edu\.cn\/UserLogin\.aspx\?preURL\='

    HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    def __init__(self):
        self._s = requests.session()
        self._s.headers = self.HEADERS
        self.__check()

    def __check(self):
        r = self._s.get(self.URL_NEWS)
        if re.search(self.URL_PRE, r.url):
            self.__login(r.text)

    def __login(self, html):
        post_data = {
            'ctl00$ContentPlaceHolder1$userEmail':'********', #帐号密码请通过学校获取
            'ctl00$ContentPlaceHolder1$userPassWord':'********',
            'ctl00$ContentPlaceHolder1$CheckBox1':'on',
            'ctl00$ContentPlaceHolder1$Button1':'登录',
            '__VIEWSTATE':'',
            '__EVENTVALIDATION':''
        }
        dom = etree.HTML(html)
        post_data['__VIEWSTATE'] = dom.xpath('//*[@id="__VIEWSTATE"]')[0].attrib['value']
        post_data['__EVENTVALIDATION'] = dom.xpath('//*[@id="__EVENTVALIDATION"]')[0].attrib['value']
        self._s.post('http://news.gdut.edu.cn/UserLogin.aspx?preURL=http://news.gdut.edu.cn/default.aspx',data=post_data)