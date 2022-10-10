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
    
for i in [2243, 2245,2248, 2250,  2251,  2255, 2256, 2258, 2260,2261,2262, 2263, 2264,2265, 2267,2268, 2269, 2270,  2271, 2272, 2273, 2274, 2276,2277, 2278, 2279,2280, 2282, 2283, 2284, 2285, 2286,  2287, 2288, 2289, 2290, 2293, 2294, 2295, 2296, 2298, 2300,  2302, 2304,  2305,2305, 2306, 2309, 2310, 2311, 2312, 2315,2317, 2318,  2319, 2320,2322, 2324, 2325,  2326, 2327,2328, 2332,2334, 2336, 2338, 2339,  2340, 2342, 2345,2346, 2349,2350, 2351, 2352, 2354,2355,2356,2357,2358,2359, 2360, 2361, 2362, 2363, 2368, 2369, 370, 2371, 2373,2374,  2375, 2377, 2382,2384,2385, 2386, 2387, 2388, 2389, 2390, 2391,2392, 2395, 2396,2397, 2398,2399]:
    pre_pre_process(i)