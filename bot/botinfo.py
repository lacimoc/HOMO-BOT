async def main(message_data, event, _log, login_info):
    if message_data.get('message_type') == 'group':
        if message_data.get('raw_message') == ".bot":
            await event.send_group_msg(group_id=message_data['group_id'], data=f"Bot {login_info['data']['nickname']} Work on LLOneBot Designed by HOMO-Bot Ver.0.1.4(4) [Python 3.11.8 For HOMO-Bot]")

    if message_data.get('message_type') == 'private':
        if message_data.get('raw_message') == ".bot":
            await event.send_private_msg(user_id=message_data['user_id'], data=f"Bot {login_info['data']['nickname']} Work on LLOneBot Designed by HOMO-Bot Ver.0.1.4(4) [Python 3.11.8 For HOMO-Bot]")
