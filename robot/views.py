from django.shortcuts import render, HttpResponse
import time
from wxpy import *
import random
import apiai
import requests
import json


TULING_TOKEN = '87e9a5015fdb455faf26823e6f20d0eb'  # 图灵机器人key

APIAI_TOKEN = '63ae6dcab54343efac3ac31c845aa7fe'

# def bot_longin_success(request):
#     print(request)
#     return HttpResponse("OK")
#     # return render(request, 'robot/QRcode.html')




def display(request):
    bot = Bot(console_qr=True, cache_path=True, qr_path="E:\Blog\static\images\QR.jpg")
    bot.enable_puid()

    @bot.register()
    def reply(msg):
        if msg.text == '1':
            return 'I\'m Still Alive!! ' + time.strftime('%y/%m/%d-%H:%M:%S', time.localtime())
        elif msg.text == '2':
            return 'aaaa'
        else:
            url_api = 'http://www.tuling123.com/openapi/api'
            data = {
                'key': TULING_TOKEN,
                'info': msg.text,  # 收到的文字内容
                'userid': msg.sender.puid
            }
            s = requests.post(url_api, data=data).json()
            if s['code'] == 100000:
                return s['text']
            if s['code'] == 200000:
                return s['text'] + s['url']
            if s['code'] == 302000:
                news = random.choice(s['list'])
                return news['article'] + '\n' + news['detailurl']
            if s['code'] == 308000:
                menu = random.choice(s['list'])
                return menu['name'] + '\n' + menu['detailurl'] + '\n' + menu['info']

    return render(request, 'robot/QRcode.html')




def myrobot(request):
    if request.method == 'POST':
        return display(request)
    return render(request, 'robot/myrobot.html')