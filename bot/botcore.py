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
        return True

    if message_data.request_type == "friend" and message_data.post_type == "request" and conf.get('agree_friend_add') == "1":
        await event.set_friend_add_request(message_data.original_message.get('flag'), True)
        return True
    
    if message_data.msg == f"[CQ:at,qq={event.get_login_info().get('data').get('user_id')}]  .bot exit":
        await event.reply(message_data, "即将退出本群")
        await event.set_group_leave(message_data.group_id)
        return True
    
    if message_data.msg[:7] == ".master":
        if len(message_data.msg.split()) == 1:
            with open(file=f"{__file__[:-10]}master", mode='w') as f:
                import uuid
                master_key = str(uuid.uuid1())
                print(f"\n发送 .master {master_key} 进行身份认证\n")
                await event.reply(message_data, "发送终端中的命令进行认证")
                f.write(master_key)
        if len(message_data.msg.split()) == 2:
            with open(file=f"{__file__[:-10]}master", mode='r') as f:
                master_key = f.read()
                if message_data.msg.split()[1] == master_key:
                    master = open(file=f"{__file__[:-10]}master.json", mode='r')
                    master_list = json.load(master)
                    master.close()
                    master = open(file=f"{__file__[:-10]}master.json", mode='w')
                    master_list[f"{message_data.user_id}"] = 1
                    json.dump(master_list, master)
                    master.close()
                    await event.reply(message_data, "认证成功")
                else:
                    await event.reply(message_data, "无效的KEY")
    
    if message_data.msg_type == "group":
        if message_data.msg == f"[CQ:at,qq={event.get_login_info().get('data').get('user_id')}]  .bot on":
            f = open(file=f"{__file__[:-10]}block_data.json", mode='r')
            switch_dict = json.load(f)
            f.close()
            f = open(file=f"{__file__[:-10]}block_data.json", mode='w')
            switch_dict[f'{message_data.group_id}'] = 1
            json.dump(switch_dict, f)
            f.close()
            await event.reply(message_data, "开启成功")
            return False

        if message_data.msg == f"[CQ:at,qq={event.get_login_info().get('data').get('user_id')}]  .bot off":
            f = open(file=f"{__file__[:-10]}block_data.json", mode='r')
            switch_dict = json.load(f)
            f.close()
            f = open(file=f"{__file__[:-10]}block_data.json", mode='w')
            switch_dict[f'{message_data.group_id}'] = 0
            json.dump(switch_dict, f)
            f.close()
            await event.reply(message_data, "关闭成功")
            return False


        f = open(file=f"{__file__[:-10]}block_data.json", mode='r')
        switch_dict = json.load(f)
        if switch_dict.get(f'{message_data.group_id}') == None:
            switch_dict[f'{message_data.group_id}'] = 1
            f.close()
            f = open(file=f"{__file__[:-10]}block_data.json", mode='w')
            json.dump(switch_dict, f)
            f.close()
        if switch_dict.get(f'{message_data.group_id}') == 0:
            return True
        return False
    return False
