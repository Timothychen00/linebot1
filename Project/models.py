import pymongo,os,datetime
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
        self.tz=datetime.timezone(datetime.timedelta(hours=+8))
    
    def create(self,form):
        id=self.customers.find().sort("_id",pymongo.DESCENDING).limit(1)[0]['_id']+1
        data={
            "_id":id,
            "name":form.name.data,
            "phone":form.phone.data,
            "telephone":form.telephone.data,
            'machine':form.machine.data,
            "address":form.address.data,
            "next-time":form.next_time.data,
            "note":form.note.data,
            "logs":{}
        }
        self.customers.insert_one(data)
        print(id)

    def delete(self,id):
        print('delete')
        if id:
            self.customers.delete_one({"_id":id})

    def change_data(self,key,value,form):
        data={
            "name":form.name.data,
            "phone":form.phone.data,
            "telephone":form.telephone.data,
            "address":form.address.data,
            'machine':form.machine.data,
            "next-time":form.next_time.data,
            "remark":form.note.data,
        }
        self.customers.update_one({key:value},{'$set':data})

    def add_log(self,key,value,update_data,next_time,date=None):
        result=self.search(key,value)[0]
        print(result)
        result=result['logs']
        if not date:
            date=datetime.datetime.now(self.tz).strftime("%Y-%m-%d")
        if result:
            result[date]=update_data
            print(result)
            print(self.customers.update_one({key:value},{"$set":{"logs":result}}))
            self.customers.update_one({key:value},{"$set":{"next-time":next_time}})
            print("update success")
        else:
            print('not existed')


    def search(self,key=None,value=None):
        if key and value:
            results=self.customers.find({key:value})
        else:
            results=self.customers.find()
        results=list(results)
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

class Server_Logger:
    def __init__(self):
        pass
    
    def write_log(self):
        pass
    
    def change_path(self):
        pass