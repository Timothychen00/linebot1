from flask import Blueprint, redirect,render_template,url_for,flash,session,request,jsonify
from Project.forms import LoginForm,FinishForm,DelayForm,CustomerForm
from Project.models import User,db_model
import datetime
from Project.decorators import login_required
from dateutil.relativedelta import relativedelta
app_route=Blueprint("app_route",__name__,static_folder='static',template_folder='templates')

@app_route.before_request
def print_url():
    print("url:",request.url)

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
    if not form.next_time.data:
        form.next_time.data='0000-00'
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
        data=['完成',form.component.data,form.person.data,form.note.data,form.fee.data]
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
        data=['延期','',form.person.data,"延期至:"+str(form.next_time.data)+'      '+form.note.data,'']
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
    # print('--'*20,'\n',request.url)
    if request.method=='GET':
        key=request.args.get('key')
        value=request.args.get('value')
        type=request.args.get('type')
        month=request.args.get('month')
        start=request.args.get('start')
        data_length=request.args.get('length')
        try:
            if key=='_id':
                value=int(value)
        except:
            pass
        try:
            data_length=int(data_length)
            start=int(start)
        except:
            pass
        print(key,value,type,start,data_length,month)

        results=db_model.search(key,value,month)
        print(len(results))
        if type=='str':
            if results and len(results)==1:
                return "找到一個結果"
            elif results:
                return "有多個結果"
            else:
                return "沒有找到"
        elif type=='json':
            if not data_length:
                data_length=len(results)
            if not start:
                start=0
            print("length:",data_length)
            processed_results=[]
            end=data_length+start
            if data_length+start>len(results):
                end=len(results)
            for i in range(start,end):
                processed_results.append([results[i]["_id"],results[i]["name"],results[i]["phone"],results[i]["address"]])
            # print(results)
            processed_results.insert(0,month)
            return jsonify(processed_results)
    
    elif request.method=='POST':
        print(form.validate_on_submit())
        if form.validate_on_submit():
            flash('新增成功')
            db_model.create(form)
        else:
            flash('新增失敗')
        return redirect('/customers/')
    return render_template('user-manage.html',results=results,form=form,month=month,next_id=db_model.next_id())

@app_route.route("/customers/<int:id>/")
@login_required
def each_customer(id):
    print(id)
    result=db_model.search('_id',id)[0]
    print("result:",result)
    related_results=db_model.search('name',result['name'])
    print("related:",related_results)
    related=[]
    length=len(related_results)
    for i in range(length):
        related.append([str(related_results[i]['_id']),str(related_results[i]['name'])])
    result['logs']=sorted(result['logs'].items(), key=lambda x:x[0])
    
    return render_template('each-customer.html',result=result,related=related)

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
    related_results=db_model.search('name',result['name'])
    related=[]
    length=len(related_results)
    for i in range(length):
        related.append(str(related_results[i]['_id']))
    if form.validate_on_submit():
        db_model.change_data('_id',id,form)
        flash("修改成功")
        return redirect("/customers/"+str(id)+'/')
    return render_template('each-customer-edit.html',form=form,result=result,related=related)

@app_route.route('/import')
@login_required
def import_dd():
    db_model.import_data('test','csv',1)
    return '1'

@app_route.route('/customers/output/')
@login_required
def output_data():
    month=request.args.get('month',None)
    db_model.output_data(month,filename=month)
    
    host=request.host
    if host!='127.0.0.1:8000':
        host="https://"+host
    
    return redirect('/static/'+month+'.xlsx')

@app_route.route("/customers/<int:id>/delete_log")
@login_required
def delete_log(id):
    log_id=request.args.get('log_id')
    print(log_id)
    log_id=int(log_id)
    date=request.args.get('date')
    print(id,log_id,date)
    db_model.delete_log(id,date,log_id)
    
    host=request.host
    if host!='127.0.0.1:8000':
        host="https://"+host
    return redirect(host+'/customers/'+str(id)+"/#logs")

@app_route.route("/backup")
@login_required
def backup():
    db_model.backup_data()
    flash('備份完成')
    return redirect('/home')

@app_route.before_request
def e():
    print("-"*20)