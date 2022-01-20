from flask import Flask,request,abort,render_template
# from linebot import LineBotApi,WebhookHandler
# from linebot.models import TextSendMessage,MessageEvent,TextMessage
# from linebot.exceptions import LineBotApiError,InvalidSignatureError
# import pymongo,os
# from dotenv import load_dotenv
# load_dotenv()


# client = pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.mgwi6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

app=Flask(__name__)



# db = client.Flask
# collection=db.settings
# result=collection.find_one()

# print(result)
# line_bot_api = LineBotApi('Qi7XZPL25/HKPXECrtPOJjA3mwTPAkS+eppoWlXNDhAEVe4qmyuTX7tsdjgBA9z27xzOyPo+eqP5oJMCf6+Gz1S5JzisSb2A9Viap0sWrajVfWAeld1ZefrGjWOWFOtcPZLLmsb4SYPmHV+pdrP8ygdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('3d35c2610fb78762643b8b7a58414ba7')
@app.route('/')
def home():
    return render_template('home.html')



@app.route('/messages')
def messages():
    return 'fuck'

# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         print("Invalid signature. Please check your channel access token/channel secret.")
#         abort(400)

#     return 'OK'


# def load_settings():
#     collection=db.settings
#     result=collection.find_one()
#     settings=result

if __name__=='__main__':
    app.run(debug=True)