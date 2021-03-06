import pymongo,os,random,time
from dotenv import load_dotenv
test_size=1
st_time=time.time()
load_dotenv()
client = pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.Flask
collection=db.customers
collection.delete_many({})#clear documents in customers
date=["2022-01-26","2022-01-29","2022-01-27","2022-01-30","2022-04-26","2022-07-16","2022-06-06","2022-09-23"]
ans_notify=random.choices(list(range(1,test_size+1)),k=5)
ans_task=random.choices(list(range(1,test_size+1)),k=5)
all=[]
city=['台北市','新北市','台中市','基隆市']
area=['淡水區','中正區','信義區','仁愛區']
for i in range(1,test_size+1):
    data={
        '_id':i,
        'name':"陳澤榮",
        'phone':'09'+''.join(random.sample("1234567890",8)),
        'telephone':''.join(random.sample("1234567890",8)),
        'address':random.sample(city,1)[0]+random.sample(area,1)[0],
        'last-time':'2021-03',
        'next-time':"2022-04",
        'note':"我要當立法委員",
        'logs':
        {
            '2022-01-30':["完成",['A','B','C'],'人員',"不好用","3500NT"],
        }
    }
    
    all.append(data)
print(all)
collection.insert_many(all)
#output answers
with open('./test_ans.txt','w') as f1:
    f1.write("ans_notify="+str(ans_notify))
    f1.write("\nans_task="+str(ans_task))
e_time=time.time()
print(e_time-st_time)