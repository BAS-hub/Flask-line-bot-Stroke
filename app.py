from flask import Flask, request, abort
import os
from linebot.models import *
from linebot import *
import json
import requests

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['YOUR_CHANNEL_SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    # print(body['events'][0]['replyToken'])
    reply_token = req['events'][0]['replyToken']
    message = req['events'][0]['message']
    if message['type'] == 'text' and message['text'] == 'covid' :
        reply_covid(reply_token)
    else :
        line_bot_api.reply_message(reply_token, TextSendMessage(text='สวัสดีครับ from basnaja 😇'))

    return 'OK'
def reply_covid(reply_token):
    data = requests.get('http://covid19.th-stat.com/json/covid19v2/getTodayCases.json')
    json_data = json.loads(data.text)
    date = json_data['UpdateDate']
    confirm = json_data['NewConfirmed']
    recoverd = json_data['NewRecovered']
    death = json_data['NewDeaths']
    line_bot_api.reply_message(reply_token, TextSendMessage(text='Covid news {}\nConfirm {}\nRecoverd {}\nDeath {}'.format(date,confirm,recoverd,death)))

if __name__ == "__main__":
    app.run()
