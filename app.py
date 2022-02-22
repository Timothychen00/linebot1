from flask import Flask
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from ProjectPackage.config import Config
from ProjectPackage.routes import app_route
from ProjectPackage.tools import process_search_data
from ProjectPackage import parameter
from linebot.models import TextSendMessage

app=Flask(__name__,static_folder='ProjectPackage/static/',template_folder='ProjectPackage/templates/')
parameter.settings
#scheduler
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
app.config.from_object(Config())
app.register_blueprint(app_route)#register blueprint
# app.secret_key='123456789'

parameter.load_settings()

def job3():
    results=parameter.search()
    tokens=parameter.settings['user-id']
    for token in tokens:
        parameter.line_bot_api.push_message(token,TextSendMessage(text=process_search_data(results)+"\n搜索耗時:\n"+results[2]))
    print(datetime.datetime.now(parameter.timezone).strftime("%H %M %S"))
    
if parameter.settings['notification-time']:
    scheduler.add_job(id='jobx', func=job3, trigger='cron', day='*',hour=parameter.settings['notification-time'].split(":")[0],minute=parameter.settings['notification-time'].split(":")[1])


scheduler.init_app(app)
scheduler.start()
if __name__=='__main__':#不要把東西放在__name__這個if裡面，因為如果使用gunicorn啟動部署伺服器那__name__永遠不會是__main__
    app.run(use_reloader=False,debug=True,port=8080)

