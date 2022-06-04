import pandas
import os,pymongo,sys,datetime
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
load_dotenv()

client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.Flask
collection=db.customers
checked=1
err=[]
multi=[]
def output_sample(df):
    import os 
    if os.path.exists('a.xlsx'):
        os.remove('a.xlsx')
    with pandas.ExcelWriter("a.xlsx", engine="openpyxl", mode="w") as writer:
        df.to_excel(writer,'a')

def process_data(id):
    try:
        id_str=str(id).zfill(3)
        print('-'*20,"\n\n\nid:",id_str)

        dataframe=pandas.read_excel('vip/A'+id_str+'.xlsx')
        print(dataframe)

        #整理資料位置
        columns=len(dataframe.columns)
        pointer=1
        times=1
        while pointer<columns:
            if str(dataframe.iat[2,pointer])!='nan':
                for j in range(2,9):
                    dataframe.iat[j,times]=dataframe.loc[j][pointer]
                    dataframe.iat[j,pointer]=float('nan')
                times+=1
            pointer+=1
        output_sample(dataframe)
        print(dataframe.loc[2])

        data={
            '_id':'',
            'name':'',
            'phone':'',
            'address':'',
            'machine':'',
            'note':'',
            'note1':'',
            'note-set':'',
            'last-time':'',
            'next-time':'',
            'logs':{}
        }

        label=[
                #column1
                [
                    ("客戶編號","_id"),
                    ("客戶名稱",'name'),
                    ('聯絡電話','phone'),
                    ('地址','address'),
                    ('','note'),
                    ('保養','note1')
                ],
                #column2
                [
                    ('客戶類別','machine'),
                    ('','machine'),
                    ('行動電話','phone'),
                    [('','note'),('聯絡人','phone'),('抬頭','note')],
                    [("FAX",'note'),('統編','note')],
                    ('備註','note')
                ],
                #column3
                [
                    ('','machine'),
                    ('',''),
                    ('安裝日期','note-set'),
                    ('電話','phone'),
                    ('抬頭','note'),
                    ('統編','note')
                ]
            ]

        # err=[]#saving error messages
        for i in range(3):#column
        #list means it contains multiple sections
        #tuple means it represent a small pair
            for j in range(len(label[i])):
                if str(dataframe.loc[2+j][i])!='nan':#not empty
                    print(label[i][j][0])
                    now_pairs=label[i][j]
                    data_type=type(now_pairs)
                    
                    if data_type is tuple:#single possible
                        if now_pairs[0] in str(dataframe.loc[2+j][i]):#not suit for the field
                            temp=dataframe.loc[2+j][i]#temp_data
                            if now_pairs[1] =='_id':
                                temp=id
                            elif now_pairs[1]!='note':
                                temp=temp.split(':')[-1].split('：')[-1].replace(' ','')
                            if temp:
                                if now_pairs[1] and data[now_pairs[1]]:
                                    separate=','
                                    if now_pairs[1]=='note':
                                        separate='\n------------------------------------\n'
                                    elif now_pairs[1]=='machine':
                                        separate='/'
                                    data[now_pairs[1]]+=(separate+temp)
                                else:
                                    data[now_pairs[1]]=temp
                        else:
                            err.append(['_id',id,'excel資料存在問題或資料未填寫'])
                    else:#multi-possible
                        for pair in now_pairs:#each pair
                            if pair[0] in dataframe.loc[2+j][i]:#not suit for the field
                                temp=dataframe.loc[2+j][i]#temp_data
                                if pair[1] =='_id':
                                    temp=id
                                elif pair[1]!='note':
                                    temp=temp.split(':')[-1].split('：')[-1].replace(' ','')
                                print('temp-------',temp)
                                if temp:
                                    if pair[1] and data[pair[1]]:
                                        separate=','
                                        if pair[1]=='note':
                                            separate='\n------------------------------------\n'
                                        elif pair[1]=='machine':
                                            separate='/'
                                        data[pair[1]]+=(separate+temp)
                                    else:
                                        data[pair[1]]=temp


        print(dataframe.loc[len(dataframe)-2])

        last_row=dataframe.loc[len(dataframe)-1]
        #sum_money--------------
        sum=0
        ## find end
        pointer=0
        if len(dataframe)-1!=9:
            for col in range(len(last_row)-1,0,-1):
                if str(last_row[col])!='nan':
                    pointer=col
                    break
            print(pointer)
            ## sum
            for log_index in range(9,len(dataframe)):
                if str(dataframe.loc[log_index][pointer])!='nan':
                    try:
                        sum+=int(dataframe.loc[log_index][pointer])
                    except:
                        continue

            sum_time=dataframe.loc[len(dataframe)-1][0]
            if str(last_row[0])=='nan':
                sum_time=dataframe.loc[len(dataframe)-2][0]
            sum_time=int(sum_time)
        else:
            sum_time=0
        print('共',sum_time,sum)
        #sum_money--------------

        last_time=''
        if sum_time:
            last_time=dataframe.loc[len(dataframe)-1][1]
            if str(last_time)=='nan':
                last_time=dataframe.loc[len(dataframe)-2][1]

            #parse lasttime
            print('lasttime:',last_time)
            last_time=str(last_time).split('.')
            last_time[1]=last_time[1].zfill(2)
            if len(last_time)==3:
                last_time[2]=last_time[2].zfill(2)
            last_time[0]=str(int(last_time[0])+1911)
            last_time=str(last_time[:])[1:-1].replace(',','-').replace(' ','').replace('\"','').replace('\'','')
            print('lasttime:',last_time)
        else:
            if not('>' in data['note-set']) and data['note-set']:
                set_time=str(data['note-set'])
                set_time.replace(' ','')
                set_time=set_time.split('.')
                set_time[0]=str(int(set_time[0])+1911)
                last_time=str(set_time[:])[1:-1].replace(',','-').replace(' ','').replace('\"','').replace('\'','')
            else:
                err.append(['_id',id,'安裝時間錯誤'])

        print('lasttime:',last_time)

        #每一道的部件
        temp=''
        for i in range(2,8):
            print(dataframe.loc[9])
            arr=dataframe.loc[9][i].split("道")
            print(arr)
            if len(arr)==2:
                arr[1]=arr[1].replace(':','').replace('\n','')
                if arr[1]:
                    temp+=(arr[0]+"道:"+arr[1].replace(' ','')+'\n')
            else:
                err.append(['_id',id,'arr每一道'])
        if temp!='':
            data['note']+=('\n------------------------------------\n'+temp[:-1])
        print(temp)

        data['last-time']=last_time

        duration=data['note1']
        number=[('十一',11),('一',1),('二',2),('三',3),('四',4),('五',5),('六',6),('七',7),('八',8),('九',9)]
        past_time=data['last-time']
        
        count=len(past_time)
        print('ct',count)
        filter='%Y-%m-%d'
        if count==10:
            end=count
        else:
            end=-1*(10-count)
        if data['last-time']:
            if str(duration)!='nan' and duration!='':
                if '年' in duration and '月' in duration:
                    err.append(['_id',id,'保養年月都有'])
                else:
                    if '年' in duration:
                        duration=duration.split('年')[0]
                        duration=duration.split(':')[-1]
                        if '半' in duration:
                            data['next-time']=str(datetime.datetime.strptime(past_time,filter[:end])+relativedelta(months=6)).split(' ')[0][:-3]
                        else:
                            data['next-time']=str(datetime.datetime.strptime(past_time,filter[:end])+relativedelta(years=int(duration))).split(' ')[0][:-3]

                    elif '月' in duration:
                        duration=duration.split('個')[0]
                        duration=duration.split(':')[-1]
                        data['next-time']=str(datetime.datetime.strptime(past_time,filter[:end])+relativedelta(months=int(duration))).split(' ')[0][:-3]
                    else:
                        duration=''
                        err.append(['_id',id,'保養週期不符合格式'])

        print('duration',duration)

        data['note']+=('\n------------------------------------\n'+'共'+str(sum_time)+"次   "+str(sum)+"NT")
        data['note']="保養週期:"+data['note1']+'\n------------------------------------\n'+data['note']
        data['note']="安裝日期:"+data['note-set']+'\n------------------------------------\n'+data['note']
        data['_id']=id
        
        #upload data
        if collection.find({"_id":id}):
            collection.delete_one({"_id":id})
        collection.insert_one(data)
        print(data)

            #check multi sheets
        if checked:
            xls = pandas.ExcelFile('vip/A'+id_str+'.xlsx')
            print(xls.sheet_names)
            if len(xls.sheet_names)>1:
                df = pandas.read_excel('vip/A'+id_str+'.xlsx', sheet_name=xls.sheet_names[1])
                if len(df)>1:
                    multi.append(['_id',id])
    except:
        err.append(['_id',id,'報錯無法處理'])
        
# test_list=[239,242,244,270,274,286,367,392,406,423,456,478,490,491]
test_list=[1014,1084,1087,1118,1220,1227,1229,1244,1247,1248,1249,1250,1253,1259,1264,1283,1307,1310,1326,1349,1363,1373,1424,1437,1451,1457,1473,1513,1651,1654,1688,1760,1762,1787]

for i in sys.argv:
    if 'uncheck' in i:
        checked=0

for i in sys.argv:
    if '-id=' in i:
        i=i.replace('-id=','')
        process_data(int(i))
        break
else:
    for k in test_list:
        process_data(k)
            
print('-'*20,'\nerrors:')
for item in err:
    print(item)
    
print('-'*20,'\nmulti:')
for item in multi:
    print(item)