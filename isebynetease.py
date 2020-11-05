# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import wave
import base64
import hashlib
import json
from imp import reload

import time

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/iseapi'
APP_KEY = ''  # your app key
APP_SECRET = '' # your app secret

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size-10:size]

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def connect(audio_file_path,audio_text):
    recordname=audio_file_path.split("/")[-1]
    audio_file_path = audio_file_path
    lang_type = 'en' #当前仅支持英文
    extension = audio_file_path[audio_file_path.rindex('.')+1:]
    if extension != 'wav':
        print('不支持的音频类型')
        sys.exit(1)
    wav_info = wave.open(audio_file_path, 'rb')
    sample_rate = wav_info.getframerate()
    nchannels = wav_info.getnchannels()
    wav_info.close()
    with open(audio_file_path, 'rb') as file_wav:
        q = base64.b64encode(file_wav.read()).decode('utf-8')

    data = {}
    data['text'] = audio_text
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['signType'] = "v2"
    data['langType'] = lang_type
    data['rate'] = sample_rate
    data['format'] = 'wav'
    data['channel'] = nchannels
    data['type'] = 1

    response = do_request(data)
    j = json.loads(str(response.content, encoding="utf-8"))
    print(j)
    #句子完整度
    contextIntegrity="句子完整度:"+str( round(j["integrity"], 2))+"  "
    pronunciation="发音准确度:"+str(round(j["pronunciation"],2))+"  "
    fluency="流利度:"+str(round(j["fluency"],2))+"  "
    speed="语速:" +str(round(j["speed"],2))+" "
    recordAndResult=recordname+" "+contextIntegrity+pronunciation+fluency+speed+"\n"
    # print(recordAndResult)
    #
    resul_file = open('./result'+ '/result_' + recordname.split('.')[0] + '.txt', 'w',encoding='utf-8').write(str(j))
    # print(resul_file)

    return recordAndResult


