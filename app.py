from flask import Flask,request,abort,render_template
from linebot import LineBotApi,WebhookHandler
from linebot.models import TextSendMessage,MessageEvent,TextMessage,StickerMessage,StickerSendMessage
from linebot.exceptions import LineBotApiError,InvalidSignatureError
import pymongo,os,random
from dotenv import load_dotenv
from debug.json_formal_3 import json_formal_output
from debug.debug_tool import message_event_debug
from re import match
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import datetime,time
from config import Config
from routes import app_route
load_dotenv()

client = pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
tz=datetime.timezone(datetime.timedelta(hours=+8))
app=Flask(__name__)

db = client.Flask
# users=set()
settings=dict()
line_bot_api = LineBotApi(os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])
commands=["!bot help","!bot bind","!bot unbind","!bot reload settings","!bot now bounded","!bot search","!bot settings"]
today_notify={}#今日提醒的日期
today_task={}#今日待完成的日期
notification=[]
task=[]

#scheduler
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

app.register_blueprint(app_route)
@app.route('/settings/reload')
def load_settings():
    global settings
    collection=db.settings
    result=collection.find_one()
    settings=result
    return "settings reloaded"

def search():
    global today_notify,today_task,notification,task
    notification=[]#今日通知內容
    task=[]#今日待更換內容
    today_notify={}#今日通知應該的日期
    today_task={}#今日待更換應該的日期
    collection=db.customers
    results=collection.find()
    st_time=time.time()
    #先獲取提醒、代辦應該的時間
    for component in settings['component-lifetime'].keys():
        today_notify[component]=datetime.datetime.strftime(datetime.datetime.now(tz)+datetime.timedelta(days=settings['days-in-advance']),"%Y-%m-%d")
        today_task[component]=datetime.datetime.strftime(datetime.datetime.now(tz),"%Y-%m-%d")
    for customer in results:#找到即輸出
        for component,next_date in customer['component'].items():
            if next_date==today_notify[component]:
                notification.append([customer['_id'],component,next_date,customer['phone'],customer['address']])
            elif next_date==today_task[component]:
                task.append([customer['_id'],component,next_date,customer['phone'],customer['address']])
    end_time=time.time()
    duration=end_time-st_time
    print(notification)
    print(task)
    json_formal_output(str(notification).replace('\'','\"'),'debug/notification.json')
    json_formal_output(str(task).replace('\'','\"'),'debug/task.json')
    print(duration)
    label=['編號',"姓名","下次更換日期","聯繫方式","地址"]
    label=str(label)
    label=label[1:-1].replace(','," ")
    label=label.replace('\'',"")
    return notification,task,str(duration),label

load_settings()


def job3():
    results=search()
    tokens=settings['user-id']
    for token in tokens:
        line_bot_api.reply_message(token,TextSendMessage(text=process_search_data(results)+"\n搜索耗時:\n"+results[2]))
    print(datetime.datetime.now(tz).strftime("%H %M %S"))
if settings['notification-time']:
    scheduler.add_job(id='jobx', func=job3, trigger='cron', day='*',hour=settings['notification-time'].split(":")[0],minute=settings['notification-time'].split(":")[1])

def process_search_data(results):
    text='今天提醒:\n'
    if results[0]:
        text+=results[3]+"\n"
        for each_notify in results[0]:
            print(each_notify)
            for each_content in each_notify:
                text+=str(each_content)+"  "
            text+="\n"
    else:
        text+="無\n"
    text+="\n今日待更換:\n"
    if results[1]:
        text+=results[3]+"\n"
        for each_task in results[1]:
            print(each_task)
            for each_content in each_task:
                text+=str(each_content)+"  "
            text+="\n"
    else:
        text+="無\n"
    return text

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
    reply_token=event.reply_token

    if match("!bot bind",message):
        if event.source.type=="group":
            if not event.source.group_id in settings['user-id']:
                settings['user-id'].append(event.source.group_id)
        else:
            if not event.source.user_id in settings['user-id']:
                settings['user-id'].append(event.source.user_id)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已綁定"))
        update_settings("user-id")#強制更新

    elif match("!bot unbind",message):
        load_settings()
        if event.source.type=='group':
            if event.source.group_id in settings['user-id']:
                settings['user-id'].remove(event.source.group_id)
        else:
            if event.source.user_id in settings['user-id']:
                settings['user-id'].remove(event.source.user_id)
        line_bot_api.reply_message(reply_token,TextSendMessage(text="done!"))
        update_settings("user-id")#強制更新

    elif match("!bot help",message):
        line_bot_api.reply_message(reply_token,TextSendMessage(text="Available Commands:\n"+str(commands)))
    elif match("!bot reload settings",message):
        load_settings()
        line_bot_api.reply_message(reply_token,TextSendMessage(text="reload settings"))
    elif match("!bot now bounded",message):
        line_bot_api.reply_message(reply_token,TextSendMessage(text=str(settings['user-id'])))
    elif match("!bot search",message):
        results=search()
        line_bot_api.reply_message(reply_token,TextSendMessage(text=process_search_data(results)+"\n搜索耗時:\n"+results[2]))
    elif match("!bot settings",message):
        line_bot_api.reply_message(reply_token,TextSendMessage(text="已經綁定的用戶:\n"+str(settings['user-id'])+"\n\n提醒提前天數:"+str(settings['days-in-advance'])+"\n\n提醒時間:"+settings['notification-time']+"\n\n部件壽命:\n"+str(settings['component-lifetime'])))
    elif match("!bot profile index=",message):
        print(message)
        message=message.split("index=")
        profile=line_bot_api.get_profile(settings['user-id'][int(message[1])])
        line_bot_api.reply_message(reply_token,TextSendMessage(text="username:\n"+profile.display_name+"\n\nuser_id:\n"+profile.user_id+"\n\npicture_url:\n"+profile.picture_url))
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
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(use_reloader=False,debug=True,port=8080)

