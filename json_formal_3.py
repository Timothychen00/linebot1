def json_formal_output(jsonString,output_filename,input_filename='none'):
    if not jsonString:
        with open(input_filename,'r')as file1:
            jsonString=file1.read()

    enterChar=[',','{','[','}',']']#所有的特殊字元
    nowIndent=[0,0]
    indentWidth=4
    stringChar=['\'','\"']#自傳的識別字元
    pointer=0#表示目前所在字串的位置
    inString=[False,False]#表示是否位於字串中（是的話就忽略）

    for i in jsonString:
        #檢測是否位於自傳
        if i =='\'':
            inString[0]=not inString[0]
        elif i =='\"':
            inString[1]=not inString[1]
        #在特殊字元後加入\n，忽略在字串中的可能性
        #後面插入
        if i in enterChar[:3] and inString[0]==False and inString[1]==False:
            jsonString=jsonString[:pointer+1]+'\n'+jsonString[pointer+1:]#在目前字元後面加入換行
            pointer+=1
        #前面插入
        if i in enterChar[3:] and inString[0]==False and inString[1]==False:
            jsonString=jsonString[:pointer]+'\n'+jsonString[pointer:]#在目前字元後面加入換行
            pointer+=1
        pointer+=1

    jsonString=jsonString.split('\n')
    #縮排+輸出檔案
    with open(output_filename,'w')as file2:
        for eachline in jsonString:
            inString=[False,False]
            pointer=0
            for char in eachline:
                if char =='\'':
                    inString[0]=not inString[0]
                elif char =='\"':
                    inString[1]=not inString[1]
                #增加縮排（，不影響縮排所以忽略）
                if char in enterChar[1:3] and inString[0]==False and inString[1]==False:
                    nowIndent[1]+=1
                #減少縮排
                elif char in enterChar[3:] and inString[0]==False and inString[1]==False:
                    nowIndent[1]-=1
                    nowIndent[0]-=1
                pointer+=1
            file2.write((nowIndent[0]*indentWidth*" ")+eachline+'\n')
            nowIndent[0]=nowIndent[1]

