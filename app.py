from flask import Flask
from flask import render_template
from linebot import (
    LineBotApi, WebhookHandler
)
app=Flask(__name__)

# app.static_folder='static'

@app.route('/')
def home():
    return render_template('home.html')

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')

@app.route('/messages')
def home():
    return 'fuck'


if __name__=='__main__':
    app.run()