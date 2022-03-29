from flask import flash, redirect,session
from functools import wraps
import datetime

def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if 'logged_in' in session and session['logged_in']:
            return a(*args,**kwargs)
        else:
            flash('請先登入')
            return redirect('/')
    return wrap

# def log_out(a):
#     def wrap(*args,**kwargs):
#         time=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8))).strftime("%Y-%m-%d %H:%M:%S")
#         print('[',time,']')
#         a(*args,**kwargs)
    
#     return wrap