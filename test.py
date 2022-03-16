from email import header
from linebot.models import TextSendMessage,MessageEvent,TextMessage,StickerMessage,StickerSendMessage,FollowEvent,MessageAction,MessageTemplateAction,TemplateSendMessage,TemplateAction,ButtonsTemplate,UnfollowEvent,QuickReply,QuickReplyButton,ImageSendMessage
from linebot import LineBotApi,WebhookHandler
from flask import Flask,request,abort
from linebot.exceptions import LineBotApiError,InvalidSignatureError
import re,time,os
from dotenv import load_dotenv

load_dotenv()
line_bot_api=LineBotApi(os.environ['access_token'])
handler=WebhookHandler(os.environ['channel_secret'])

app=Flask(__name__)
main='sss'
users={}
img_url=[
    'https://i.imgur.com/FxKCVOp.png',
    'https://i.imgur.com/qSwqvTf.png',
    'https://i.imgur.com/RrzQye1.jpg',
    'https://i.imgur.com/6CdmNA6.jpg',
    'https://i.imgur.com/QgsgOXh.jpg',
    'https://i.imgur.com/UwyIOQd.jpg'
    
]

profile_data = {'Authorization': 'Bearer ' + 'LmaavfrIszrPWuHNBf3SFPeMfnrgJccgFN8hiRuzUjUApokgonk3Oc+kJTFGLuL9JbDruJiWWN3Q7Ao7bR0vlShJSOGSf3h1PZ7a4K3RsAzygrwb8voToNvLSKiIitzcmFhWwr7hgu5unjAn/bxrpgdB04t89/1O/w1cDnyilFU='}
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def reply(tx):
    return QuickReply(items=[QuickReplyButton(action=MessageAction(label=tx,text=tx))])

@handler.add(MessageEvent,message=TextMessage)
def process(event):
    global users
    print(event.source.user_id,'|',event.message.text)
    times=users[event.source.user_id]
    # print(str(line_bot_api.get_profile(user_id=event.source.user_id,header=profile_data)['displayName']),'|',event.message.text)
    if re.match("開始遊戲",event.message.text) and users[event.source.user_id]==0:
        message=[]
        message.append(TextSendMessage(text="你是一個生活在江西省某所高中的高中生。成績也就是全校倒數幾名，對於你來說每天必不可少的就是和電腦待在一起。"))
        message.append(TextSendMessage(text='你家裡只有一台電腦（在父母的房間），而你基本上每天都花14個小時在電腦前玩各種遊戲，時間就這樣過去，你的近視越來越深，而身體狀況也越來越差'))
        message.append(TextSendMessage(text='在社會上對於這種人，有著一種稱呼“網癮少年”。而你的父母也發現了異常，自從初三開始“阿藤”對電子產品的成癮現象越來越明顯，甚至常常上課上到一半就直接翹課回家打電腦。'))
        message.append(TextSendMessage(text='而為了防止這一切的發生，父母在上班的時候都會把路由器鎖在保險箱裡再離開。這天父母又去上班了，你也抗拒不了成癮反應，開始在家裡尋找能夠打遊戲的方式',quick_reply=reply("Hi,Siri 那我應該怎麼辦？")))
        line_bot_api.reply_message(event.reply_token,message)
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==1:
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='讓我想想'),TextSendMessage(text='你爸不是把路由器鎖在客廳的保險箱了嗎',quick_reply=reply("好像是這樣。（走到保險箱前）"))])
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==2:
        line_bot_api.reply_message(event.reply_token,[ImageSendMessage(original_content_url=img_url[1],preview_image_url=img_url[1],quick_reply=reply("哇，我不知道密碼"))])
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==3:
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='我分析了保險箱的結構，這是1970年產的保險箱，這個型號應該是需要輸入4個英文字母，才能打開，不知道會不會對你有些幫助',quick_reply=reply("毫無頭緒"))])
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==4:
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='可能要在外面找些線索，可是感覺好像也沒什麼線索了 ',quick_reply=reply("等等保險箱下面好像壓著什麼（拿了出來）"))])
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==5:
        line_bot_api.reply_message(event.reply_token,[ImageSendMessage(original_content_url=img_url[2],preview_image_url=img_url[2]),TextSendMessage(text='這看起來像是一張密碼表',quick_reply=reply("好像需要對應什麼"))])
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==6:
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='真假',quick_reply=reply("笑死"))])
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==7:
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='。。。。。'),TextSendMessage(text='**請輸入4位英文字母的密碼**')])
        users[event.source.user_id]+=1
    elif users[event.source.user_id]==8:
        if re.match("我好笨，我需要協助",event.message.text):
                line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="確實"),TextSendMessage(text="保險箱上面好像有一行字")])
        elif not re.match("NOPE",event.message.text):
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='嗶嗶嗶嗶，密碼好像錯誤了。'),TextSendMessage(text='再嘗試一下吧',quick_reply=reply("我好笨，我需要協助"))])
            return
        else:
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='嗶嗶嗶嗶，密碼正確，保險箱好像開了'),ImageSendMessage(original_content_url=img_url[0],preview_image_url=img_url[0]),TextSendMessage(text='那應該就是路由器了，可是上面寫著一行字，看起來又不怎麼像wifi密碼（印象中好像是10位的數字）')])
            users[event.source.user_id]+=1
    elif users[event.source.user_id]==9:
        if re.match("我好笨，我需要協助",event.message.text):
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="確實"),TextSendMessage(text="總感覺跟物理課背的兩串數字好像有點關聯")])
        elif not re.match("1049273603",event.message.text):
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='嗶嗶嗶嗶，密碼好像錯誤了。'),TextSendMessage(text='再嘗試一下吧',quick_reply=reply("我好笨，我需要協助"))])
            return
        else:
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='啊啊啊啊啊啊，連上了～～～～～～',quick_reply=reply("水"))])
            users[event.source.user_id]+=1
    elif users[event.source.user_id]==10:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='未完待續............'))

@handler.add(FollowEvent)
def follow(event):
    print("in Follow")
    if not(event.source.user_id in users.keys()):
        users[event.source.user_id]=0
    print(users)
    button_template_message =ButtonsTemplate(thumbnail_image_url="https://png.pngtree.com/element_our/20200702/ourlarge/pngtree-game-start-stereo-icon-button-image_2292214.jpg",
                                    title='來玩場遊戲吧～', 
                                    text='準備一下吧',
                                    image_size="cover",
                                    actions=[
                                        MessageTemplateAction(
                                            label='開始遊戲', text='開始遊戲'
                                        ),
                                    ]
                                )
    line_bot_api.reply_message(
        event.reply_token,[
        TextSendMessage(text="歡迎追蹤～～～～～～～"),
        TextSendMessage(text="準備好了嗎，請點擊  “開始遊戲”"),
        TemplateSendMessage(
            alt_text="err",
            template=button_template_message
        )]
    )

@app.route("/")
def home():
    return users

@handler.add(UnfollowEvent)
def follow(event):
    if (event.source.user_id in users.keys()):
        del users[event.source.user_id]
        
if __name__=="__main__":
    app.run(port=8080)