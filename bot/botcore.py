# -*- coding: utf-8 -*-

import os
import json

try:
    with open(file=os.getcwd()+"\\conf\\event_conf.json", mode='r') as event_conf:
        conf = json.load(event_conf)
        if conf == None:
            raise FileNotFoundError
except FileNotFoundError:
    with open(file=os.getcwd()+"\\conf\\event_conf.json", mode='w') as event_conf:
        json.dump({"agree_group_invite":"0", "agree_friend_add":"0"}, event_conf)
        raise FileNotFoundError
    

async def bot_core_event(message_data, event):
    print(message_data.sub_type)
    if message_data.sub_type == "invite" and conf.get('agree_group_invite') == "1":
        await event.set_group_add_request(message_data.original_message.get('flag'), message_data.original_message.get('sub_type'), True)
        return None

    if message_data.sub_type == "invite" and conf.get('agree_friend_add') == "1":
        await event.set_friend_add_request(message_data.original_message.get('flag'), True)
        return None
    
    if message_data.msg == f"[CQ:at,qq={event.get_login_info().get('data').get('user_id')}].bot exit":
        await event.reply(message_data, "即将退出本群")
        await event.set_group_leave(message_data.group_id)
    
