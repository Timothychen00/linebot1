import pymongo,os
from dotenv import load_dotenv
from flask import flash,request,session
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
        if id:
            self.customers.delete_one({"_id":id})
    
    def change_data(self,form):
        pass
    
    def add_log():
        pass

    def search(self,key,value):
        if key:
            results=self.customers.find({key:value})
        else:
            results=self.customers.find()
        return results

db_model=DB_Model()
    
class User():
    def start_session(self):
        pass
    
    def login(self,username,password):
        result=db_model.users.find_one({'username':username})
        if result:
            if check_password_hash(result['password'],password):
                self.start_session()
            else:
                return {"password":"密碼錯誤"}
        else:
            return {'username':"帳號不存在"}

    def logout():
        pass
    
    def register(self,username,password):#only for back-end change
        db_model.users.insert_one({'username':username,'password':generate_password_hash(password)})
        pass
    
for each in db_model.search("_id",1):
    print(each)
    print()

db_model.delete('1')
# User().register('timothychen','123123123')
