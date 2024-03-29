# -*- coding: utf-8 -*-

import os
import json

from bot import log

try:
    with open(file=os.getcwd()+"\\conf\\config.json", mode='r') as conf:
        listen_port = json.load(conf).get('listen_port')
        if listen_port == None:
            raise FileNotFoundError
except FileNotFoundError:
    with open(file=os.getcwd()+"\\conf\\config.json", mode='w') as conf:
        json.dump({"report_port":"","listen_port":""}, conf)
        raise FileNotFoundError

async def post(url, data=None):
    import requests_async as requests
    await requests.post(url=url,data=data)


class event():
    def set_block():
        class BreakLoop(Exception):
            pass
        log.logger.info("[BotCore] <set_block> Done")
        raise BreakLoop
    

    async def reply(message_data, data):
        if message_data.msg_type == "group":
            log.logger.info(f"[BotAPI] <reply> GroupMessage: {message_data.group_id} Message: {data}")
            url = f"http://127.0.0.1:{listen_port}/send_group_msg"
            data = {"group_id":f"{message_data.group_id}", "message":f"{data}"}
            
            return await post(url=url, data=data)
        
        if message_data.msg_type == "private":
            log.logger.info(f"[BotAPI] <reply> PrivateMessage: {message_data.user_id} Message: {data}")
            url = f"http://127.0.0.1:{listen_port}/send_private_msg"
            data = {"user_id":f"{message_data.user_id}", "message":f"{data}"}
            
            return await post(url=url, data=data)

    
    async def send_group_msg(group_id, data, type=0):
        if type != 0:
            log.logger.info(f"[BotAPI] <reply> GroupMessage: {group_id} Message: {data}")
            url = f"http://127.0.0.1:{listen_port}/send_group_msg"
            data = {"group_id":f"{group_id}", "message":[{"type":f"{type}", "data":{"text":f"{data}"}}]}

            return await post(url=url, data=data)
        else:
            log.logger.info(f"[BotAPI] <reply> GroupMessage: {group_id} Message: {data}")
            url = f"http://127.0.0.1:{listen_port}/send_group_msg"
            data = {"group_id":f"{group_id}", "message":f"{data}"}
    
            return await post(url=url, data=data)
    

    async def send_private_msg(user_id, data, type=0):
        if type != 0:
            log.logger.info(f"[BotAPI] <reply> PrivateMessage: {user_id} Message: {data}")
            url = f"http://127.0.0.1:{listen_port}/send_private_msg"
            data = {"user_id":f"{user_id}", "message":[{"type":f"{type}", "data":{"text":f"{data}"}}]}

            return await post(url=url, data=data)
        else:
            log.logger.info(f"[BotAPI] <reply> PrivateMessage: {user_id} Message: {data}")
            url = f"http://127.0.0.1:{listen_port}/send_private_msg"
            data = {"user_id":f"{user_id}", "message":f"{data}"}

            return await post(url=url, data=data)


    async def delete_msg(message_id):
        log.logger.info(f"[BotAPI] <delete_msg> MessageID: {message_id} Done")
        url = f"http://127.0.0.1:{listen_port}/delete_msg"
        data = {"message_id":message_id}
        return await post(url=url, data=data)


    def get_login_info():
        import json
        import requests

        url = f"http://127.0.0.1:{listen_port}/get_login_info"
        login_info = requests.post(url=url)
        if login_info.status_code != 200:
            return None
        return json.loads(login_info.content.decode('utf-8'))
    

    def get_group_list():
        import json
        import requests

        url = f"http://127.0.0.1:{listen_port}/get_group_list"
        group_list = requests.post(url=url)
        if group_list.status_code != 200:
            return None
        return json.loads(group_list.content.decode('utf-8').get('data'))
    

    def get_group_info(group_id):
        import requests

        url = f"http://127.0.0.1:{listen_port}/get_group_info"
        data = {"group_id":group_id}
        group_info = requests.post(url=url,data=data)
        if group_info.status_code != 200:
            return None
        return json.loads(group_info.content.decode('utf-8').get('data'))
    

    def get_group_member_list(group_id):
        import requests

        url = f"http://127.0.0.1:{listen_port}/get_group_member_list"
        data = {"group_id":group_id}
        group_member_list = requests.post(url=url,data=data)
        if group_member_list.status_code != 200:
            return None
        return json.loads(group_member_list.content.decode('utf-8').get('data'))
    

    def get_group_member_info(group_id, user_id):
        import requests

        url = f"http://127.0.0.1:{listen_port}/get_group_member_info"
        data = {"group_id":group_id, "user_id":user_id}
        return json.loads(requests.post(url=url, data=data).content.decode('utf-8')).get('data')
    

    def get_friend_list():
        import requests

        url = f"http://127.0.0.1:{listen_port}/get_friend_list"
        friend_list = requests.post(url=url)
        if friend_list.status_code != 200:
            return None
        return json.loads(friend_list.content.decode('utf-8').get('data'))
    

    def get_msg(message_id):
        import requests

        url = f"http://127.0.0.1:{listen_port}/get_msg"
        data = {"message_id":message_id}
        msg = requests.post(url=url, data=data)
        if msg.status_code != 200:
            return None
        return json.loads(msg.content.decode('utf-8'))
    

    def send_like(user_id, times=1):
        import requests

        url = f"http://127.0.0.1:{listen_port}/send_like"
        data = {"user_id":user_id, "times":times}
        status = requests.post(url=url, data=data).status_code
        if status == 200:
            log.logger.info("[BotAPI] <send_like> Done")
        else:
            log.logger.info("[BotAPI] <send_like> Fail")

    
    async def set_group_ban(group_id, user_id, duration=60):
        url = f"http://127.0.0.1:{listen_port}/set_group_ban"
        data = {"group_id":group_id, "user_id":user_id, "duration":duration}
        await post(url=url, data=data)
        log.logger.info("[BotAPI] <set_group_ban> Done")


    async def set_group_leave(group_id):
        url = f"http://127.0.0.1:{listen_port}/set_group_leave"
        data = {"group_id":group_id}
        await post(url=url, data=data)
        log.logger.info(f"[BotAPI] <set_group_leave> {group_id} Done")

    
    async def set_group_kick(group_id, user_id):
        url = f"http://127.0.0.1:{listen_port}/set_group_kick"
        data = {"group_id":group_id, "user_id":user_id}
        await post(url=url, data=data)
        log.logger.info(f"[BotAPI] <set_group_kick> kick {user_id} from {group_id} Done")


    async def set_group_add_request(flag, sub_type, approve):
        url = f"http://127.0.0.1:{listen_port}/set_group_add_request"
        data = {"flag":flag, "sub_type":sub_type, "approve":approve}
        await post(url=url, data=data)
        log.logger.info(f"[BotAPI] group_invite accept Done")

        
    async def set_friend_add_request(flag, approve):
        url = f"http://127.0.0.1:{listen_port}/set_friend_add_request"
        data = {"flag":flag, "approve":approve}
        await post(url=url, data=data)
        log.logger.info(f"[BotAPI] friend_request accept Done")
