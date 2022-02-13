import pymongo,os
from linebot import LineBotApi,WebhookHandler
from dotenv import load_dotenv
load_dotenv()
client = pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Flask

line_bot_api = LineBotApi(os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])