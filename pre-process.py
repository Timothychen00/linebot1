import pandas,os

tlist=[74,77,85,94,100,102,106,108,109,113,115,118,122,124,128,132,142,146,147,148,150,158,161,162,164,165,172,176,177,183,189]

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