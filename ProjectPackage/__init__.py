import pymongo,os
from linebot import LineBotApi,WebhookHandler
from dotenv import load_dotenv
from ProjectPackage.debug.json_formal_3 import json_formal_output
import time,datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from ProjectPackage.linebot_control import job3

load_dotenv()
class Parameter:
    def __init__(self):
        # linebot
        self.line_bot_api=LineBotApi(os.environ['Channel_access_token'])
        self.handler=WebhookHandler(os.environ['Channel_secret'])
        # db
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db=self.client.Flask
        # settings
        self.settings={}
        self.notification_predict={}
        self.task_predict={}
        self.notification=[]
        self.task=[]
        self.bot={}
        self.bot['commands']=["!bot help","!bot bind","!bot unbind","!bot reload settings","!bot now bounded","!bot search","!bot settings"]
        self.timezone=datetime.timezone(datetime.timedelta(hours=+8))
        
        self.scheduler=APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
        
    def update_settings(self,key):
        collection=self.db.settings
        print(self.settings)
        print(self.settings['user-id'])
        collection.update_one({'type':"settings"},{"$set":{key:self.settings[key]}})

    def load_settings(self):
        collection=parameter.db.settings
        result=collection.find_one()
        self.settings=result
        if self.settings['notification-time']:
            self.scheduler.add_job(id='jobx', func=job3, trigger='cron', day='*',hour=parameter.settings['notification-time'].split(":")[0],minute=parameter.settings['notification-time'].split(":")[1])
        return "settings reloaded"
    
    def search(self):
        self.notification=[]#今日通知內容
        self.task=[]#今日待更換內容
        self.notification_predict={}#今日通知應該的日期
        self.task_predict={}#今日待更換應該的日期
        collection=parameter.db.customers
        results=collection.find()
        st_time=time.time()
        #先獲取提醒、代辦應該的時間
        for component in parameter.settings['component-lifetime'].keys():
            self.notification_predict[component]=datetime.datetime.strftime(datetime.datetime.now(self.timezone)+datetime.timedelta(days=self.settings['days-in-advance']),"%Y-%m-%d")
            self.task_predict[component]=datetime.datetime.strftime(datetime.datetime.now(self.timezone),"%Y-%m-%d")
        for customer in results:#找到即輸出
            for component,next_date in customer['component'].items():
                if next_date==self.notification_predict[component]:
                    self.notification.append([customer['_id'],component,next_date,customer['phone'],customer['address']])
                elif next_date==self.task_predict[component]:
                    self.task.append([customer['_id'],component,next_date,customer['phone'],customer['address']])
        end_time=time.time()
        duration=end_time-st_time
        print(self.notification)
        print(self.task)
        json_formal_output(str(self.notification).replace('\'','\"'),'./notification.json')
        json_formal_output(str(self.task).replace('\'','\"'),'./task.json')
        print(duration)
        label=['編號',"姓名","下次更換日期","聯繫方式","地址"]
        label=str(label)
        label=label[1:-1].replace(','," ")
        label=label.replace('\'',"")
        return self.notification,self.task,str(duration),label

parameter=Parameter()