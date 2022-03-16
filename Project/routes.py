from flask import Blueprint, redirect,render_template,url_for
from Project.forms import LoginForm
from Project.models import User

app_route=Blueprint("app_route",__name__,static_folder='static',template_folder='templates')


@app_route.route("/",methods=['GET','POST'])#login
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        print(username)
        print(password)
        result=User().login(username,password)
        if result:
            if 'username' in result.keys():
                form.username.errors.append(result['username'])
            if 'password' in result.keys():
                form.password.errors.append(result['password'])
        else:
            print('sec')
            return redirect("home")
    return render_template("login.html",form=form)

#Home page
@app_route.route("/finish/",methods=['GET','POST'])
def finish():
    return '1'

@app_route.route("/delay/",methods=['GET','POST'])
def delay():
    return '2'

@app_route.route("/home")
def home():
    return render_template('base.html')

@app_route.route("/customers/")
def customers_manage():
    pass

#Customers Page
@app_route.route("/customers/this_month/")
def this_month():
    pass

@app_route.route("/customers/next_month/")
def next_month():
    pass

@app_route.route("/customers/<id>/")
def each_customer(id):
    pass

@app_route.route("/customers/<id>/delete/")
def delete_customer(id):
    pass

@app_route.route("/customers/create/",methods=['GET','POST'])
def create_customer():
    pass