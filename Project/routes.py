from flask import Blueprint
app_route=Blueprint("app_route")


@app_route.route("/",methods=['GET','POST'])#login
def login():
    return '1'

#Home page
@app_route.route("/finish/",methods=['GET','POST'])
def finish():
    return '1'

@app_route.route("/delay/",methods=['GET','POST'])
def delay():
    return '2'

@app_route.route("/home")
def home():
    return "1"

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