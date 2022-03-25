from flask import Blueprint, redirect,render_template,url_for,flash,session,request
from sympy import false
from Project.forms import LoginForm,FinishForm,DelayForm,CustomerForm
from Project.models import User,db_model
import datetime
from Project.decorators import login_required
app_route=Blueprint("app_route",__name__,static_folder='static',template_folder='templates')

@app_route.route("/",methods=['GET','POST'])#login
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        print(username)
        print(password)
        rememberme=form.rememberme.data
        result=User().login(username,password)
        if result:
            if 'username' in result.keys():
                form.username.errors.append(result['username'])
            if 'password' in result.keys():
                form.password.errors.append(result['password'])
        else:
            if rememberme:
                session.permanent = True
                app_route.permanent_session_lifetime = datetime.timedelta(days=20)
            else:
                session.permanent=True
                app_route.permanent_session_lifetime = datetime.timedelta(minutes=5)
            return redirect("home")
    return render_template("login.html",form=form)

@app_route.route('/logout')
@login_required
def logout():
    User().logout()
    return redirect('/')

#Home page
@app_route.route("/finish/",methods=['GET','POST'])
@login_required
def finish():
    form=FinishForm()
    if form.validate_on_submit():
        print('type',form.key_type.data)
        print('key',form.key.data)
        print('state',form.state.data)
        print('component',form.component.data)
        print('finish',form.finish_time.data)
        print('next',form.next_time.data)
        print('note',form.note.data)
        return 'sent'
    return render_template('finish.html',form=form)

@app_route.route("/delay/",methods=['GET','POST'])
@login_required
def delay():
    form=DelayForm()
    if form.validate_on_submit():
        for i in form:
            print(i,i.data)
        return 'sent'
    return render_template('delay.html',form=form)

@app_route.route("/home")
@login_required
def home():
    return render_template('base.html')

@app_route.route("/customers/")
@login_required
def customers_manage():
    key=request.args.get('key',None)
    value=request.args.get('value',None)
    print(key,value)
    results=db_model.search(key,value)
    return render_template('user-manage.html',results=list(results))

#Customers Page
@app_route.route("/customers/this_month/")
@login_required
def this_month():
    pass

@app_route.route("/customers/next_month/")
@login_required
def next_month():
    pass

@app_route.route("/customers/<int:id>/")
@login_required
def each_customer(id):
    print(id)
    results=list(db_model.search('_id',id))[0]
    print(results)
    return render_template('each-customer.html',result=results)

@app_route.route("/customers/<int:id>/delete/")
@login_required
def delete_customer(id):
    db_model.delete(id)
    flash('刪除成功')
    return redirect('/customers/')
    

@app_route.route("/customers/create/",methods=['GET','POST'])
@login_required
def create_customer():
    form=CustomerForm()
    if form.validate_on_submit():
        return form
    return render_template('settings.html',form=form)