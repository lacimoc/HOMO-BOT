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
    

async def bot_core_event(message_data, event) -> bool:
    if message_data.sub_type == "invite" and conf.get('agree_group_invite') == "1":
        await event.set_group_add_request(message_data.original_message.get('flag'), message_data.original_message.get('sub_type'), True)
        return False

    if message_data.request_type == "friend" and message_data.post_type == "request" and conf.get('agree_friend_add') == "1":
        await event.set_friend_add_request(message_data.original_message.get('flag'), True)
        return False
    
    if message_data.msg == f"[CQ:at,qq={event.get_login_info().get('data').get('user_id')}] .bot exit":
        await event.reply(message_data, "即将退出本群")
        await event.set_group_leave(message_data.group_id)
        return False
    
    if message_data.msg_type == "group":
        if message_data.msg == f"[CQ:at,qq={event.get_login_info().get('data').get('user_id')}] .bot on":
            f = open(file=f"{__file__[:-10]}block_data.json", mode='r')
            switch_dict = json.load(f)
            f.close()
            f = open(file=f"{__file__[:-10]}block_data.json", mode='w')
            switch_dict[f'{message_data.group_id}'] = 1
            json.dump(switch_dict, f)
            f.close()
            await event.reply(message_data, "开启成功")
            return True

        if message_data.msg == f"[CQ:at,qq={event.get_login_info().get('data').get('user_id')}] .bot off":
            f = open(file=f"{__file__[:-10]}block_data.json", mode='r')
            switch_dict = json.load(f)
            f.close()
            f = open(file=f"{__file__[:-10]}block_data.json", mode='w')
            switch_dict[f'{message_data.group_id}'] = 0
            json.dump(switch_dict, f)
            f.close()
            await event.reply(message_data, "关闭成功")
            return True


        f = open(file=f"{__file__[:-10]}block_data.json", mode='r')
        switch_dict = json.load(f)
        if switch_dict.get(f'{message_data.group_id}') == None:
            switch_dict[f'{message_data.group_id}'] = 1
            f.close()
            f = open(file=f"{__file__[:-10]}block_data.json", mode='w')
            json.dump(switch_dict, f)
            f.close()
        elif switch_dict.get(f'{message_data.group_id}') == 0:
            return True
        return False
    return False
