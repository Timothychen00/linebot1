import pandas,os,sys

if len(sys.argv)>1 and '-id=' in sys.argv[1]:
    sys.argv[1]=sys.argv[1].split('-id=')[-1]
    tlist=[int(sys.argv[1])]
else:
    tlist=[2243, 2245,2248, 2250,  2251,  2255, 2256, 2258, 2260,2261,2262, 2263, 2264,2265, 2267,2268, 2269, 2270,  2271, 2272, 2273, 2274, 2276,2277, 2278, 2279,2280, 2282, 2283, 2284, 2285, 2286,  2287, 2288, 2289, 2290, 2293, 2294, 2295, 2296, 2298, 2300,  2302, 2304,  2305,2305, 2306, 2309, 2310, 2311, 2312, 2315,2317, 2318,  2319, 2320,2322, 2324, 2325,  2326, 2327,2328, 2332,2334, 2336, 2338, 2339,  2340, 2342, 2345,2346, 2349,2350, 2351, 2352, 2354,2355,2356,2357,2358,2359, 2360, 2361, 2362, 2363, 2368, 2369, 370, 2371, 2373,2374,  2375, 2377, 2382,2384,2385, 2386, 2387, 2388, 2389, 2390, 2391,2392, 2395, 2396,2397, 2398,2399]
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