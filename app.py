from flask import Flask,request,abort,render_template
from linebot import LineBotApi,WebhookHandler
from linebot.models import TextSendMessage,MessageEvent,TextMessage,StickerMessage,StickerSendMessage
from linebot.exceptions import LineBotApiError,InvalidSignatureError
import pymongo,os,random
from dotenv import load_dotenv
from json_formal_3 import json_formal_output
from debug_tool import message_event_debug
from re import match
load_dotenv()

client = pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

app=Flask(__name__)

db = client.Flask
# users=set()
settings=dict()
line_bot_api = LineBotApi(os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])
commands=["!bot help","!bot bind","!bot unbind","!bot reload settings","!bot now bounded"]

@app.route('/settings/reload')
def load_settings():
    global settings
    collection=db.settings
    result=collection.find_one()
    settings=result

load_settings()

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/<name>")
def name(name):
    global settings
    print(settings['user-id'])
    line_bot_api.push_message(list(settings['user-id']),TextSendMessage(text="終於"))
    return name

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def echo(event):
    global settings
    message_event_debug(event,str(settings['user-id']))
    message=event.message.text
    collection=db.settings
    reply_token=event.reply_token

    if match("!bot bind",message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已綁定"))
        if event.source.type=="group":
            if not event.source.group_id in settings['user-id']:
                settings['user-id'].append(event.source.group_id)
        else:
            if not event.source.user_id in settings['user-id']:
                settings['user-id'].append(event.source.user_id)
        print(settings['user-id'])
        collection.update_one({"type":"settings"},{"$set":{"user-id":list(settings['user-id'])}})

    elif match("!bot unbind",message):
        load_settings()
        if event.source.type=='group':
            if event.source.group_id in settings['user-id']:
                settings['user-id'].remove(event.source.group_id)
        else:
            if event.source.user_id in settings['user-id']:
                settings['user-id'].remove(event.source.user_id)
        line_bot_api.reply_message(reply_token,TextSendMessage(text="done!"))
        update_settings("user-id")

    elif match("!bot help",message):
        line_bot_api.reply_message(reply_token,TextSendMessage(text="Available Commands:\n"+str(commands)))
    elif match("!bot reload settings",message):
        load_settings()
        line_bot_api.reply_message(reply_token,TextSendMessage(text="reload settings"))
    elif match("!bot now bounded",message):
        line_bot_api.reply_message(reply_token,TextSendMessage(text=str(settings['user-id'])))
    # else:
    #     line_bot_api.reply_message(reply_token,TextSendMessage(text=event.message.text))


@handler.add(MessageEvent,message=StickerMessage)
def f(event):
    message_event_debug(event)
    line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=446,sticker_id=random.choice(list(range(2001,2027)))))

def update_settings(key):
    global settings
    collection=db.settings
    print(settings)
    print(settings['user-id'])
    collection.update_one({'type':"settings"},{"$set":{key:settings[key]}})



if __name__=='__main__':
    app.run(debug=True,port=8080)

#Ucdb272bac34b11e2d1b3b8c88af2325e蘇昱誠
#U6feaa10ddbb90decf621c4feb49e351c陳澤榮