from ProjectPackage import parameter
from linebot.models import TextSendMessage,MessageEvent,TextMessage,StickerMessage,StickerSendMessage
from ProjectPackage.debug.debug_tool import message_event_debug
from ProjectPackage.tools import process_search_data
import random,re,datetime

@parameter.handler.add(MessageEvent,message=TextMessage)
def echo(event):
    message_event_debug(event,str(parameter.settings['user-id']))
    message=event.message.text
    reply_token=event.reply_token

    if re.match("!bot bind",message):
        if event.source.type=="group":
            if not event.source.group_id in parameter.settings['user-id']:
                parameter.settings['user-id'].append(event.source.group_id)
        else:
            if not event.source.user_id in parameter.settings['user-id']:
                parameter.settings['user-id'].append(event.source.user_id)
        parameter.line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已綁定"))
        parameter.update_settings("user-id")#強制更新

    elif re.match("!bot unbind",message):
        parameter.load_settings()
        if event.source.type=='group':
            if event.source.group_id in parameter.settings['user-id']:
                parameter.settings['user-id'].remove(event.source.group_id)
        else:
            if event.source.user_id in parameter.settings['user-id']:
                parameter.settings['user-id'].remove(event.source.user_id)
        parameter.line_bot_api.reply_message(reply_token,TextSendMessage(text="done!"))
        parameter.update_settings("user-id")#強制更新

    elif re.match("!bot help",message):
        parameter.line_bot_api.reply_message(reply_token,TextSendMessage(text="Available Commands:\n"+str(parameter.bot['commands'])))
    elif re.match("!bot reload settings",message):
        parameter.load_settings()
        parameter.line_bot_api.reply_message(reply_token,TextSendMessage(text="reload settings"))
    elif re.match("!bot now bounded",message):
        parameter.line_bot_api.reply_message(reply_token,TextSendMessage(text=str(parameter.settings['user-id'])))
    elif re.match("!bot search",message):
        results=parameter.search()
        parameter.line_bot_api.reply_message(reply_token,TextSendMessage(text=process_search_data(results)+"\n搜索耗時:\n"+results[2]))
    elif re.match("!bot settings",message):
        parameter.line_bot_api.reply_message(reply_token,TextSendMessage(text="已經綁定的用戶:\n"+str(parameter.settings['user-id'])+"\n\n提醒提前天數:"+str(parameter.settings['days-in-advance'])+"\n\n提醒時間:"+parameter.settings['notification-time']+"\n\n部件壽命:\n"+str(parameter.settings['component-lifetime'])))
    elif re.match("!bot profile index=",message):
        print(message)
        message=message.split("index=")
        profile=parameter.line_bot_api.get_profile(parameter.settings['user-id'][int(message[1])])
        parameter.line_bot_api.reply_message(reply_token,TextSendMessage(text="username:\n"+profile.display_name+"\n\nuser_id:\n"+profile.user_id+"\n\npicture_url:\n"+profile.picture_url))

@parameter.handler.add(MessageEvent,message=StickerMessage)
def f(event):
    message_event_debug(event)
    parameter.line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=446,sticker_id=random.choice(list(range(2001,2027)))))


def job3():
    results=parameter.search()
    tokens=parameter.settings['user-id']
    for token in tokens:
        parameter.line_bot_api.push_message(token,TextSendMessage(text=process_search_data(results)+"\n搜索耗時:\n"+results[2]))
    print(datetime.datetime.now(parameter.timezone).strftime("%H %M %S"))
    