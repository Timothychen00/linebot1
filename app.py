from flask import Flask
from Project.routes import app_route
import os

app=Flask(__name__,static_folder='Project/static/',template_folder='Project/temlpates/')
app.secret_key=os.environ['secret']#os.urandom(16).hex()
app.register_blueprint(app_route)

if __name__=='__main__':#不要把東西放在__name__這個if裡面，因為如果使用gunicorn啟動部署伺服器那__name__永遠不會是__main__
    app.run(use_reloader=False,debug=True,port=5000)

