from flask import flash, redirect,session
from functools import wraps
import datetime
import time

def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if 'logged_in' in session and session['logged_in']:
            return a(*args,**kwargs)
        else:
            flash('請先登入')
            return redirect('/')
    return wrap

def time_it(a):
    def wrap(*args,**kwargs):
        ts=time.time()
        result=a(*args,**kwargs)
        te=time.time()
        print("執行時間：",te-ts)
        return result
    return wrap