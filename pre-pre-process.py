import pandas,os,sys

def pre_pre_process(id):
    id_str=str(id).zfill(3)
    dataframe=pandas.read_excel('vip/A'+id_str+'.xlsx')
    # print(dataframe)
    for i in range(len(dataframe)):
        if str(dataframe.loc[i][5])!='nan' and str(dataframe.loc[i][5]):
            if '備註' in str(dataframe.loc[i][5]):
                if str(dataframe.loc[i+1][5])!='nan' and str(dataframe.loc[i+1][5])!='':
                    print('有備註 下面','id:',id,'|',i,'|',dataframe.loc[i][5],dataframe.loc[i+1][5])
                if str(dataframe.loc[i][6])!='nan' and str(dataframe.loc[i][6])!='':
                    os.system('python3 pre-process.py -id='+str(id))
                    print('有備註 右邊','id:',id,'|',i,'|',dataframe.loc[i][5],dataframe.loc[i][6])
    
for i in [239,242,244,270,274,286,367,392,406,423,456,478,490,491]:
    pre_pre_process(i)