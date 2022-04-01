from flask import Blueprint, redirect,render_template,url_for,flash,session,request
from Project.forms import LoginForm,FinishForm,DelayForm,CustomerForm
from Project.models import User,db_model
import datetime
from Project.decorators import login_required
from dateutil.relativedelta import relativedelta
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
    print('-'*20,'type',form.key.data)
    print('key',form.value.data)
    print('state',form.state.data)
    print('component',form.component.data)
    print('finish',form.finish_time.data)
    print('next',form.next_time.data)
    print('note',form.note.data)
    if form.validate_on_submit():
        state=form.state.data
        key=form.key.data
        value=form.value.data
        date=form.finish_time.data
        date=date.strftime("%Y-%m-%d")
        try:
            if key=='_id':
                value=int(value)
        except:
            pass
        data=['完成',form.component.data,form.note.data,form.fee.data]
        db_model.add_log(key,value,update_data=data,next_time=form.next_time.data,date=date)
        print('-'*20)
        return redirect('/home')
    return render_template('finish.html',form=form)

@app_route.route("/delay/",methods=['GET','POST'])
@login_required
def delay():
    form=DelayForm()
    if form.validate_on_submit():
        state=form.state.data
        key=form.key.data
        value=form.value.data
        try:
            if key=='_id':
                value=int(value)
        except:
            pass
        data=['延期','',"下一次更換時間:"+str(form.next_time.data)+'\n'+form.note.data,'']
        db_model.add_log(key,value,data,next_time=form.next_time.data)
        return redirect('/home')
    return render_template('delay.html',form=form)

@app_route.route("/home")
@login_required
def home():
    return render_template('base.html')

@app_route.route("/customers/",methods=['GET',"POST"])
@login_required
def customers_manage():
    form=CustomerForm()

    if request.method=='GET':
        key=request.args.get('key',None)
        value=request.args.get('value',None)
        type=request.args.get('type',None)
        try:
            if key=='_id':
                value=int(value)
        except:
            pass
        print(key,value)
        results=db_model.search(key,value)
        if type=='json':
            if results and len(results)==1:
                return "found"
            elif results:
                return "too many"
            else:
                return "not found"
    elif request.method=='POST':
        print(form.validate_on_submit())
        if form.validate_on_submit():
            flash('新增成功')
            db_model.create(form)
        else:
            flash('新增失敗')
        return redirect('/customers/')
    return render_template('user-manage.html',results=results,form=form)

#Customers Page
@app_route.route("/customers/this_month/")
@login_required
def this_month():
    this_month=datetime.datetime.now(db_model.tz).strftime('%Y-%m')
    print("this_month:",this_month)
    results=db_model.search('next-time',this_month)
    print(results)
    return render_template('user-manage.html',results=results)

@app_route.route("/customers/next_month/")
@login_required
def next_month():
    time_obj=datetime.datetime.now(db_model.tz)+relativedelta(months=1)
    next_month=time_obj.strftime("%Y-%m")
    results=db_model.search('next-time',next_month)
    return render_template('user-manage.html',results=results)

@app_route.route("/customers/<int:id>/")
@login_required
def each_customer(id):
    print(id)
    result=db_model.search('_id',id)[0]
    print(result)
    return render_template('each-customer.html',result=result)

@app_route.route("/customers/<int:id>/delete/")
@login_required
def delete_customer(id):
    db_model.delete(id)
    flash('刪除成功')
    print(id)
    return redirect('/customers/')
    
@app_route.route("/customers/<int:id>/edit/",methods=['GET','POST'])
@login_required
def change_customer(id):
    form=CustomerForm()
    result=db_model.search('_id',id)[0]
    if form.validate_on_submit():
        db_model.change_data('_id',id,form)
        flash("修改成功")
        return redirect("/customers/"+str(id)+'/')
    return render_template('each-customer-edit.html',form=form,result=result)

@app_route.route('/import')
def import_dd():
    db_model.import_data('test','csv',1)
    return '1'