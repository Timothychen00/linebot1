import pandas,os,sys

if len(sys.argv)>1 and '-id=' in sys.argv[1]:
    sys.argv[1]=sys.argv[1].split('-id=')[-1]
    tlist=[int(sys.argv[1])]
else:
    tlist=[1014,1084,1087,1118,1205,1220,1227,1229,1244,1247,1248,1249,1250,1253,1259,1264,1283,1307,1310,1326,1349,1363,1373,1424,1437,1451,1457,1473,1513,1651,1654,1688,1760,1762,1787]
def pre_process(id):
    id_str=str(id).zfill(3)
    
    dataframe=pandas.read_excel('vip/A'+id_str+'.xlsx')
   
    if os.path.exists('origin.xlsx'):
        os.remove('origin.xlsx')
    dataframe.to_excel('origin.xlsx')
   
    for i in range(2,8):
        dataframe.iat[i,0]=(str(dataframe.loc[i][0]).replace(' ','')+str(dataframe.loc[i][1]).replace(' ','')+str(dataframe.loc[i][2]).replace(' ','')).replace('nan','')
        dataframe.iat[i,1]=float('nan')
        dataframe.iat[i,2]=float('nan')
    
    if str(dataframe.loc[3][6])!='nan' and str(dataframe.loc[3][6])!='':
        sep=''
        if dataframe.iat[2,5].split(':')[-1]:
            sep='/'
        dataframe.iat[2,5]+=(sep+dataframe.loc[3][6])
        dataframe.iat[3,6]=float('nan')
        pass
    
    for i in range(2,8):
        sep=''
        if dataframe.iat[2,5].split(':')[-1] and i==2:
            sep='/'
        dataframe.iat[i,5]=(str(dataframe.loc[i][5]).replace(' ','')+(sep+str(dataframe.loc[i][6])).replace(' ','')+str(dataframe.loc[i][7]).replace(' ','')).replace('nan','')
        dataframe.iat[i,6]=float('nan')
        dataframe.iat[i,7]=float('nan')
        
    for i in range(2,8):
        sep=''
        dataframe.iat[i,10]=(str(dataframe.loc[i][10]).replace(' ','')+(sep+str(dataframe.loc[i][11])).replace(' ','')+str(dataframe.loc[i][12]).replace(' ','')).replace('nan','')
        dataframe.iat[i,11]=float('nan')
        dataframe.iat[i,12]=float('nan')
    
    if os.path.exists('vip/A'+id_str+'.xlsx'):
        os.remove('vip/A'+id_str+'.xlsx')
    dataframe.to_excel('vip/A'+id_str+'.xlsx',index=False)
    print(dataframe)
    
for k in tlist:
    pre_process(k)