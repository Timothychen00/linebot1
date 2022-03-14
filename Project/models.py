import pymongo,os
from dotenv import load_dotenv
from flask import flash,request,session
from werkzeug.security import generate_password_hash,check_password_hash
load_dotenv()

class DB_Model():
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db=self.client.Flask
        self.collection=self.db.customers
    
    def create(self,form):
        id=self.collection.find().sort("_id",pymongo.DESCENDING).limit(1)[0]['_id']+1
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
        self.collection.insert_one(data)
    
    def delete(self,id):
        if id:
            self.collection.delete_one({"_id":id})
    
    def change_data(self,form):
        pass
    
    def add_log():
        pass

    def search(self,key,value):
        if key:
            results=self.collection.find({key:value})
        else:
            results=self.collection.find()
        return results

db_model=DB_Model()
    
class User():
    def start_session():
        pass
    
    def login():
        pass
    
    def logout():
        pass
    
    def register():#only for back-end change
        pass
    
for each in db_model.search("_id",1):
    print(each)
    print()

db_model.delete('1')