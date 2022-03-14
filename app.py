from flask import Flask
from ProjectPackage.config import Config
from ProjectPackage.routes import app_route
from ProjectPackage import parameter
from ProjectPackage.linebot_control import job3

app=Flask(__name__,static_folder='ProjectPackage/static/',template_folder='ProjectPackage/templates/')
parameter.settings
#scheduler
app.config.from_object(Config())
app.register_blueprint(app_route)#register blueprint

parameter.load_settings()

parameter.scheduler.init_app(app)
parameter.scheduler.start()

if __name__=='__main__':#不要把東西放在__name__這個if裡面，因為如果使用gunicorn啟動部署伺服器那__name__永遠不會是__main__
    app.run(use_reloader=False,debug=True,port=8080)

