import pandas,os
from Project.decorators import time_it

@time_it
def load_data(filename,mode):
    cols=['name','phone1','phone2','machine','next-time','address','note']
    if mode=='csv':
        dataframe=pandas.read_csv(filename+'.csv',usecols=cols)
    elif mode=='excel':
        dataframe=pandas.read_excel(filename+'.xlsx',usecols=cols)
        
    length=len(dataframe)
    data=[]
    for index in range(length):
        data.append(dataframe.loc[index].to_dict())
    # print(data)
    print('讀取模式：',mode)

print('-'*20)
print('測試資料筆數：4424筆')
load_data('test','csv')
print('-'*20)
print('測試資料筆數：4424筆')
load_data('test','excel')
print('-'*20)