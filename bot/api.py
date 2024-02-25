from bot import log

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
        import json

        if message_data.msg_type == "group":
            log.logger.info(f"[BotAPI] <reply> GroupMessage: {message_data.group_id} Message: {data}")
            url = "http://127.0.0.1:3000/send_group_msg"
            data = {"group_id":f"{message_data.group_id}", "message":f"{data}"}
            data = json.dumps(data)
            
            return await post(url=url, data=data)
        
        if message_data.msg_type == "private":
            log.logger.info(f"[BotAPI] <reply> PrivateMessage: {message_data.user_id} Message: {data}")
            url = "http://127.0.0.1:3000/send_private_msg"
            data = {"user_id":f"{message_data.user_id}", "message":f"{data}"}
            data = json.dumps(data)
            
            return await post(url=url, data=data)

    
    async def send_group_msg(group_id, data, type=0):
        import json
        
        if type != 0:
            log.logger.info(f"[BotAPI] <reply> GroupMessage: {group_id} Message: {data}")
            url = "http://127.0.0.1:3000/send_group_msg"
            data = {"group_id":f"{group_id}", "message":[{"type":f"{type}", "data":{"text":f"{data}"}}]}
            data = json.dumps(data)

            return await post(url=url, data=data)
        else:
            log.logger.info(f"[BotAPI] <reply> GroupMessage: {group_id} Message: {data}")
            url = "http://127.0.0.1:3000/send_group_msg"
            data = {"group_id":f"{group_id}", "message":f"{data}"}
            data = json.dumps(data)
    
            return await post(url=url, data=data)
    

    async def send_private_msg(user_id, data, type=0):
        import json

        if type != 0:
            log.logger.info(f"[BotAPI] <reply> PrivateMessage: {user_id} Message: {data}")
            url = "http://127.0.0.1:3000/send_private_msg"
            data = {"user_id":f"{user_id}", "message":[{"type":f"{type}", "data":{"text":f"{data}"}}]}
            data = json.dumps(data)

            return await post(url=url, data=data)
        else:
            log.logger.info(f"[BotAPI] <reply> PrivateMessage: {user_id} Message: {data}")
            url = "http://127.0.0.1:3000/send_private_msg"
            data = {"user_id":f"{user_id}", "message":f"{data}"}
            data = json.dumps(data)

            return await post(url=url, data=data)


    async def delete_msg(message_id):
        import json

        log.logger.info(f"[BotAPI] <delete_msg> MessageID: {message_id} Done")
        url = f"http://127.0.0.1:3000/delete_msg"
        data = json.dumps({"message_id":message_id})
        return await post(url=url, data=data)


    def get_login_info():
        import json
        import requests

        url = "http://127.0.0.1:3000/get_login_info"
        login_info = requests.post(url=url)
        if login_info.status_code != 200:
            return None
        return json.loads(login_info.content.decode('utf-8'))
    

    async def get_group_list():
        import json

        url = "http://127.0.0.1:3000/get_group_list"
        group_list = await post(url=url)
        if group_list.status_code != 200:
            return None
        return json.loads(group_list.content.decode('utf-8').get('data'))
    

    async def get_group_info(group_id):
        import json

        url = "http://127.0.0.1:3000/get_group_info"
        data = json.dumps({"group_id":group_id})
        group_info = await post(url=url,data=data)
        if group_info.status_code != 200:
            return None
        return json.loads(group_info.content.decode('utf-8').get('data'))
    

    async def get_group_member_list(group_id):
        import json

        url = "http://127.0.0.1:3000/get_group_member_list"
        data = json.dumps({"group_id":group_id})
        group_member_list = await post(url=url,data=data)
        if group_member_list.status_code != 200:
            return None
        return json.loads(group_member_list.content.decode('utf-8').get('data'))
    

    async def get_group_member_info(group_id, user_id):
        import json

        url = "http://127.0.0.1:3000/get_group_member_info"
        data = json.dumps({"group_id":group_id, "user_id":user_id})
        group_member_info = await post(url=url, data=data)
        if group_member_info.status_code != 200:
            return None
        return json.loads(group_member_info.content.decode('utf-8').get('data'))
    

    async def get_friend_list():
        import json

        url = "http://127.0.0.1:3000/get_friend_list"
        friend_list = await post(url=url)
        if friend_list.status_code != 200:
            return None
        return json.loads(friend_list.content.decode('utf-8').get('data'))
    

    async def get_msg(message_id):
        import json

        url = "http://127.0.0.1:3000/get_msg"
        data = json.dumps({"message_id":message_id})
        msg = await post(url=url, data=data)
        if msg.status_code != 200:
            return None
        return json.loads(msg.content.decode('utf-8').get('data'))
    

    async def send_like(user_id, times=1):
        import json

        url = "http://127.0.0.1:3000/send_like"
        data = json.dumps({"user_id":user_id, "times":times})
        status = await post(url=url, data=data).status_code
        if status == 200:
            log.logger.info("[BotAPI] <send_like> Done")
        else:
            log.logger.info("[BotAPI] <send_like> Fail")


    async def set_group_leave(group_id):
        import json

        url = "http://127.0.0.1:3000/set_group_leave"
        data = json.dumps({"group_id":group_id})
        status = await post(url=url, data=data).status_code
        if status == 200:
            log.logger.info("[BotAPI] <group_leave> Done")
        else:
            log.logger.info("[BotAPI] <group_leave> Fail")