from flask import Flask

app=Flask(__name__,static_folder='Project/static/',template_folder='Project/temlpates/')

if __name__=='__main__':#不要把東西放在__name__這個if裡面，因為如果使用gunicorn啟動部署伺服器那__name__永遠不會是__main__
    app.run(use_reloader=False,debug=True,port=8080)

