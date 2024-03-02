async def main(message_data, event, _log, login_info):
    if message_data.msg_type == 'group':
        if message_data.msg == ".bot":
            await event.send_group_msg(group_id=message_data.group_id, data=f"Bot {login_info['data']['nickname']} Work on LLOneBot Designed by HOMO-Bot Ver.0.1.7(7) [Python 3.11.8 For HOMO-Bot]")

    if message_data.msg_type == 'private':
        if message_data.msg == ".bot":
            await event.send_private_msg(user_id=message_data.user_id, data=f"Bot {login_info['data']['nickname']} Work on LLOneBot Designed by HOMO-Bot Ver.0.1.7(7) [Python 3.11.8 For HOMO-Bot]")
