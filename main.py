# @app.route('/')
# def index():
#     # obj.Response(status, status description, payload)
#     newMessage = bs.Response(200, 'success', ['asd', 1, 1,2,34,])
#     return newMessage.GetMessage()


# token : 5940972519:AAEG66kzqC5LA0-t4AlFAMJJBVVCtKvCDPo
# https://api.telegram.org/bot<Your Bot Token>/setWebhook?url=<URL that you got from Ngrok>
# https://api.telegram.org/bot5940972519:AAEG66kzqC5LA0-t4AlFAMJJBVVCtKvCDPo/setWebhook?url=https://a56a-2001-448a-5122-1fcd-74ae-f2b4-cf78-213b.ap.ngrok.io

from flask import Flask
from flask import request
from flask import Response
import requests
from chatbot import chatbot
import json
 
TOKEN = "5940972519:AAEG66kzqC5LA0-t4AlFAMJJBVVCtKvCDPo"
app = Flask(__name__)
intents = json.load(open('chatbot/intents.json', encoding="utf8"))
 
def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 
def tel_send_image(chat_id, imgUrl, caption):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': imgUrl,
        'caption': caption
    }
 
    r = requests.post(url, json=payload)
    return r
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt = parse_message(msg)
        if txt == '/start':
            tel_send_message(chat_id, 'halo, senang bertemu denganmu. kamu boleh bertanya mengenai petunjuk teknis skripsi Fakultas Ilmu Komputer Universitas Jember.\n cangkupan pengetahuan bot adalah: \n 1. Skripsi\n2. proposal skripsi\n3. teknis penulisan\n4. teknis pelaksanaan\n5. orisinalitas\n6. plagiarisme\n7. dosen pengampu bidang')
        else:
            ints = chatbot.predictClasses(txt)
            res = chatbot.getResponse(ints, intents)
            if res =='#pemetaan bidang pict':
                imgUrl = 'https://raw.githubusercontent.com/ovisannn/assetJuknis/main/pemetaan.png'
                caption ='pemetaan bidang skripsi'
                tel_send_image(chat_id, imgUrl, caption)
            else:
                tel_send_message(chat_id, res)
       
        return Response('ok', status=200)
    else:
        return "juknis skripsi fasilkom UNEJ 2022 API"
 
if __name__ == '__main__':
   app.run(debug=True)