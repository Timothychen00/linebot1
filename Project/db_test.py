import pymongo,os,random
from dotenv import load_dotenv
import time
test_size=4000
st_time=time.time()
load_dotenv()
client = pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.Flask
collection=db.customers
collection.delete_many({})#clear documents in customers
date=["2022-01-26","2022-01-29","2022-01-27","2022-01-30","2022-04-26","2022-07-16","2022-06-06","2022-09-23"]
ans_notify=random.choices(list(range(1,test_size+1)),k=5)
ans_task=random.choices(list(range(1,test_size+1)),k=5)
data={
    '_id':'1',
    'name':"Timothychen",
    'phone':"0902115275",
    'telephone':"28053457",
    'address':"新北市",
    'next-time':"2021/7",
    'remark':"caocaocaooca",
    'logs':
    {
    }
}
all=[]
for i in range(1,test_size+1):
    data['_id']=i
    data['logs']['2022-01-30']=["A,B,C","不好用","3500NT"]
    
    collection.insert_one(data)
#output answers
with open('./test_ans.txt','w') as f1:
    f1.write("ans_notify="+str(ans_notify))
    f1.write("\nans_task="+str(ans_task))
e_time=time.time()
print(e_time-st_time)