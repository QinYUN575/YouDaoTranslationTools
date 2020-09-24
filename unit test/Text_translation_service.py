# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
from importlib import reload
from rich import print
from rich.console import Console
import time
import json

console = Console()
reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '您的应用ID'
APP_SECRET = '您的应用密钥'
FROM_LANG = 'zh-CHS'
TO_LANG ='en'

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect():
    q = "中文测试文本"

    data = {}
    data['from'] = FROM_LANG
    data['to'] = TO_LANG
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    # console.log('data: ' + str(data))

    response = do_request(data)
    # print('response: ' + str(response.content.decode("utf-8")))
    # console.log('response: ' + str(response.content))

    contentType = response.headers['Content-Type']
    console.log('ContentType: ' + contentType)

    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    if contentType == 'application/json;charset=UTF-8':
        console.print('源文本:' , q)
        result = json.loads(str(response.content, encoding="utf-8"))["translation"]
        console.print('目标文本:' , result[0])
    else:
        console.log('Fail', response.content)

if __name__ == '__main__':
    connect()
