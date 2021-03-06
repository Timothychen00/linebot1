import pymongo,os,datetime,pandas
from dotenv import load_dotenv
from flask import flash,request,session
from werkzeug.security import generate_password_hash,check_password_hash
from Project.decorators import time_it
from dateutil.relativedelta import relativedelta
load_dotenv()
class DB_Model():
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.client_backup=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@drinking-bk.soibl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsAllowInvalidCertificates=True,tz_aware=True)
        self.db=self.client.Flask
        self.customers=self.db.customers
        self.users=self.db.users
        
        self.db_backup=self.client_backup.Flask
        self.customers_backup=self.db_backup.customers
        self.users_backup=self.db_backup.users
        
        self.tz=datetime.timezone(datetime.timedelta(hours=+8))
    
    def create(self,form):
        if not form.id.data:
            id=self.customers.find().sort("_id",pymongo.DESCENDING).limit(1)[0]['_id']+1
        else:
            id=int(form.id.data)
        data={
            '_id':id,
            "name":form.name.data,
            "phone":form.phone.data,
            'machine':form.machine.data,
            "address":form.address.data,
            'last-time':form.last_time.data,
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
            "address":form.address.data,
            'machine':form.machine.data,
            'last-time':form.last_time.data,
            "next-time":form.next_time.data,
            "note":form.note.data,
        }
        self.customers.update_one({key:value},{'$set':data})

    def add_log(self,key,value,update_data,next_time,date=None):
        result=self.search(key,value,False)[0]
        result=self.search('_id',result['_id'],False)[0]
        key='_id'
        value=result['_id']
        print(key,value,result)
        if not date:
            date=datetime.datetime.now(self.tz).strftime("%Y-%m-%d")
        if result:
            last=date
            result=result['logs']
            if not date in result:
                result[date]=[]
            result[date].append(update_data)
            print(result)
            
            
            if update_data[0]=='??????':
                self.customers.update_one({key:value},{"$set":{"last-time":last}})
            self.customers.update_one({key:value},{"$set":{"logs":result}})
            if next_time!='0000-00':
                self.customers.update_one({key:value},{"$set":{"next-time":next_time}})
            print("update success")
        
        else:
            print('not existed')
    
    def delete_log(self,id,date,log_id):
        result=self.search('_id',id,False)[0]
        logs=result['logs']
        del logs[date][log_id]
        self.customers.update_one({'_id':id},{"$set":{"logs":logs}})
        
    @time_it
    def search(self,key=None,value=None,month=None,sort=None,info=None):
        print('month:',month)
        print("key:",key,"value:",value)
        # print(sort)
        
        not_allowed=['\'','\"']
        #pre process
        if key!='_id' and value:
            for i in not_allowed:
                value.replace(i,"")
            value=value.split('(')[0]
            value=value.split(')')[0]
        
        if not info:
            info_dict={'_id':1,"name":1,"phone":1,"address":1}
        else:
            info_dict=info
        filter={}
        #????????????
        if key and value:
            if key =='address' or key=='phone' or key=='name':
                filter[key]={"$regex" : ".*"+value+".*"}
            else:
                filter[key]=value
        if month and month!='none':#????????????????????????????????????
            print(2)
            if month=='this_month':
                month=datetime.datetime.now(db_model.tz).strftime('%Y-%m')
            else:
                time_obj=datetime.datetime.now(db_model.tz)+relativedelta(months=1)
                month=time_obj.strftime("%Y-%m")
            filter['next-time']=month
            sort='last-time'
        else:
            sort='_id'
        #??????????????????????????????
        print('filter',filter)
        if key=='_id' and value:
            results=self.customers.find(filter)
        else:
            results=self.customers.find(filter,info_dict)
        if sort:
            print(sort)
            results=results.sort(sort,pymongo.ASCENDING)
        print(results)
        results=list(results)
        # print(results)
        return results
    
    @time_it
    def import_data(self,filename,mode,delete=0):
        cols=['name','phone','machine','last-time','next-time','address','note']
        type_dict={'name':str,'phone':str,'machine':str,'last-time':str,'next-time':str,'address':str,'note':str}
        
        if mode=='csv':
            dataframe=pandas.read_csv('./'+filename+'.csv',usecols=cols,dtype=type_dict)
        elif mode=='excel':
            dataframe=pandas.read_excel('./'+filename+'.xlsx',usecols=cols)

        if delete==1:
            self.customers.delete_many({})

        length=len(dataframe)
        data=[]
        print(self.customers.count())
        if self.customers.count():
            id=self.customers.find().sort("_id",pymongo.DESCENDING).limit(1)[0]['_id']+1
        else:
            id=1
        print(id)
        for index in range(length):
            dictionary=dataframe.loc[index].to_dict()
            dictionary['_id']=id
            dictionary['logs']={}
            data.append(dictionary)
            id+=1
        self.customers.insert_many(data)
        print('???????????????',mode)
    
    def next_id(self):
        return self.customers.find().sort("_id",pymongo.DESCENDING).limit(1)[0]['_id']+1
    
    def output_data(self,month,filename):
        results=self.search(key='next-time',value='1',month=month,sort=None,info={'last-time':1,"name":1,"phone":1,'address':1})
        # print(results)
        # print(results)
        df=pandas.DataFrame({},columns=['??????',"??????",'??????','??????'])
        for i in results:
            df.loc[len(df.index)]={"??????":i['last-time'],"??????":i['name'],"??????":i['phone'],"??????":i['address']}
        # print(df)
        df.to_excel('Project/static/'+filename+'.xlsx',encoding='utf-8',index=None)
        
    def backup_data(self):
        results=self.customers.find()
        self.customers_backup.delete_many({})
        if results:
            self.customers_backup.insert_many(list(results))
        print('done')
        
        
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
                return {"password":"????????????"}
        else:
            return {'username':"???????????????"}

    def logout(self):
        if 'logged_in' in session:
            del session['logged_in']
        if 'username' in session:
            del session['username']
    
    def register(self,username,password):#only for back-end change
        db_model.users.insert_one({'username':username,'password':generate_password_hash(password)})

# User().register(username='sinyuan75',password='03240324')