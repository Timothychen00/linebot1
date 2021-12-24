from flask import Flask
from flask import render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
app=Flask(__name__)
line_bot_api = LineBotApi('Qi7XZPL25/HKPXECrtPOJjA3mwTPAkS+eppoWlXNDhAEVe4qmyuTX7tsdjgBA9z27xzOyPo+eqP5oJMCf6+Gz1S5JzisSb2A9Viap0sWrajVfWAeld1ZefrGjWOWFOtcPZLLmsb4SYPmHV+pdrP8ygdB04t89/1O/w1cDnyilFU=')
# app.static_folder='static'

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/messages')
def messages():
    return 'fuck'
@app.route('/push')
def push():
    line_bot_api.push_message(2632205727,TextSendMessage(text='fuck'))
    return "1"



if __name__=='__main__':
    app.run()