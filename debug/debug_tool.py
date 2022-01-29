from debug.json_formal_3 import json_formal_output
def message_event_debug(event,users=False):
    json_formal_output(output_filename='debug/event.json',jsonString=str(event))#print out formal json
    print("="*20)
    #message type
    print("message_type:"+event.message.type)
    print("message:"+str(event.message))
    #id
    print("source_type:"+event.source.type)
    print("source:"+str(event.source))
    #reply
    print("reply_token:"+event.reply_token)
    #current users
    if users:
        print("users_in_var:"+users)
    print("="*20)