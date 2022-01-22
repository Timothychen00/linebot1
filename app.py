from email import message
from flask import Flask,request,abort,render_template
from linebot import LineBotApi,WebhookHandler
from linebot.models import TextSendMessage,MessageEvent,TextMessage
from linebot.exceptions import LineBotApiError,InvalidSignatureError
import pymongo,os
from dotenv import load_dotenv
from json_formal_3 import json_formal_output
import re

load_dotenv()

client = pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

app=Flask(__name__)

db = client.Flask
collection=db.settings


line_bot_api = LineBotApi(os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/<name>")
def name(name):
    global user
    print(user)
    line_bot_api.push_message(user,TextSendMessage(text="終於"))
    return name

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def echo(event):
    global user
    print(type(event))
    with open('event.json','w') as f1:
        f1.write(str(event))
    json_formal_output("event.json","output.json")
    print(event.source)
    print(event.source.user_id)
    
    if event.source.type=="group":
        user=event.source.group_id
        collection.update_one({"type":"settings"},{"$set":{"user-id":user}})
    else:
        user=event.source.user_id
        
    # print(event.source.userId)
    if(re.match("呼叫機器人",event.message.text)):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已綁定"))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    
def load_settings():
    collection=db.settings
    result=collection.find_one()
    settings=result

if __name__=='__main__':
    app.run(debug=True,port=8080)