def process_search_data(results):
    text='今天提醒:\n'
    if results[0]:
        text+=results[3]+"\n"
        for each_notify in results[0]:
            print(each_notify)
            for each_content in each_notify:
                text+=str(each_content)+"  "
            text+="\n"
    else:
        text+="無\n"
    text+="\n今日待更換:\n"
    if results[1]:
        text+=results[3]+"\n"
        for each_task in results[1]:
            print(each_task)
            for each_content in each_task:
                text+=str(each_content)+"  "
            text+="\n"
    else:
        text+="無\n"
    return text