import pymongo,os
from dotenv import load_dotenv
from flask import flash,request,session
from sympy import true
from werkzeug.security import generate_password_hash,check_password_hash
load_dotenv()
class DB_Model():
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db=self.client.Flask
        self.customers=self.db.customers
        self.users=self.db.users
    
    def create(self,form):
        id=self.customers.find().sort("_id",pymongo.DESCENDING).limit(1)[0]['_id']+1
        data={
            "_id":id,
            "name":form.name.data,
            "phone":form.phone.data,
            "telephone":form.telephone.data,
            "address":form.address.data,
            "next-time":form.next_time.data,
            "remark":form.remark.data,
            "logs":{}
        }
        self.customers.insert_one(data)
    
    def delete(self,id):
        print('delete')
        if id:
            self.customers.delete_one({"_id":id})
    
    def change_data(self,form):
        pass
    
    def add_log():
        pass

    def search(self,key=None,value=None):
        if key and value:
            if key=='_id':
                value=int(value)
            results=self.customers.find({key:value})
        else:
            results=self.customers.find()
        return results

db_model=DB_Model()
    
class User():
    def start_session(self,username):
        session['logged_in']=True
        session['username']=username
    
    def login(self,username,password):
        result=db_model.users.find_one({'username':username})
        if result:
            if check_password_hash(result['password'],password):
                self.start_session(username)
            else:
                return {"password":"密碼錯誤"}
        else:
            return {'username':"帳號不存在"}

    def logout(self):
        if 'logged_in' in session:
            del session['logged_in']
        if 'username' in session:
            del session['username']
    
    def register(self,username,password):#only for back-end change
        db_model.users.insert_one({'username':username,'password':generate_password_hash(password)})
