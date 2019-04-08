# -*- coding:utf-8 -*-

import re
import base64
import time
import hashlib
from io import BytesIO
from fontTools.ttLib import TTFont
import requests
from lxml import etree

class Xdaili(object):
    def __init__(self):
        # 订单号
        self.orderno = 'SxdkvafnkvjnklfvlkFVBAFKo'
        # 个人密钥
        self.secret = 'bdfdVLJfnv;KVAFNBLA;KNB9ac7e7'
        self.ip = "forward.xdaili.cn"
        self.port = '80'
        self.agent = self.ip + ":" + self.port

    def proxy(self):
        # 时间戳
        timestamp = str(int(time.time()))
        # 签名算法参数
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        # md5
        sign = hashlib.md5(string.encode()).hexdigest().upper()
        # auth
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        proxy = {
            "http": "http://" + self.agent,
            "https": "https://" + self.agent
        }
        return [auth, proxy]

def handlefont(page_source, prase_string):
    """
    处理字体
    """
    base64_str = re.findall("charset=utf-8;base64,(.*?)'\)", page_source)[0]
    font = TTFont(BytesIO(base64.decodebytes(base64_str.encode())))
    cmap_ = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
    handled_string = []
    try:
        for char_ in prase_string:
            decode_num = ord(char_)
            if decode_num in cmap_:
                num = cmap_[decode_num]
                num = int(num[-2:]) - 1
                handled_string.append(str(num))
            else:
                handled_string.append(char_)
        return ''.join(handled_string)
    except Exception as e:
        _ = e

def get_md5(url):
    # md5
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    pass