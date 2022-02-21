import json
# json.dump()
# json.load()
# with open("event.json",'r') as f1:
#     print(json.load(f1))
    
f1=open("event.json","r")
json.load(f1)
f1.close()

data={}
with open("test.json","w") as f2:
    
    json.dump(data,f2)