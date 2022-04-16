import pandas
df={}
df=pandas.DataFrame(df,columns=['_id',"name",'phone','address'])
df.loc[len(df.index)]={"_id":"id1","name":"name1","phone":"phone1","address":"address1"}
print(df)