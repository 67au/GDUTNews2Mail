#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from NewsLogin import NewsLogin
from lxml import etree
import json
import os
import time

class DataCmp(NewsLogin):

    KEY_MAP = {
        'hot_news' : '4',
        'hot_inform' : '5',
        'hot_msg' :'6'
    }

    def __news_iter(self):
        for key, value in self.KEY_MAP.items():
            dom = etree.HTML(self._s.post('http://news.gdut.edu.cn/ArticleList.aspx', data={'category':value}).text)
            a = dom.xpath('//*[@id="ContentPlaceHolder1_ListView1_ItemPlaceHolderContainer"]')[0]
            yield (key, [dict(id = i[0].attrib['href'].replace('./viewarticle.aspx?articleid=', ''),
                title = i[0].attrib['title'],loc = i[1].attrib['title']) for i in a])

    def cmp_result(self):
        try:
            with open('origin.json', 'r') as f:
                d = json.loads(f.read())
            tmp = {i[0]:i[1] for i in self.__news_iter()}
            output = { key:[i for i in value if i not in d[key]] for key, value in tmp.items() }
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            tmp = {i[0]:i[1] for i in self.__news_iter()}
            output = tmp
        finally:
            _j = json.dumps(tmp, indent=4, separators=(',', ':'), ensure_ascii=False)
            with open('origin.json', 'w') as f:
                f.write(_j)
            os.makedirs('Data', exist_ok=True)
            with open('Data/{}.json'.format(time.strftime('%Y%m%dT%H%M%SZ', time.localtime())), 'w') as f:
                f.write(_j)
            return output
