# -*- coding: utf-8 -*-

import time
import datetime

import bot
from bot.flask import Flask, request, jsonify
from bot import api
from bot import log
from bot import botinfo
from bot import message


import bot.log as log


from plugin import plugin_core as plugin

while True:
    try:
        login_info = api.event.get_login_info()
        if login_info != None:
            log.logger.info(f"[BotCore] BotID {login_info['data']['user_id']} named {login_info['data']['nickname']} is on ready")
            break
    except Exception:
        log.logger.warning(f"[BotCore] Fail to connect LLOneBot")
        log.logger.warning(f"[BotCore] Bot will attempt to reconnect in 10 seconds")
        time.sleep(10)


listener = Flask("ROBOT")


@listener.route('/', methods=['POST'])
async def event():
    event_data = request.json
    
    processed_message = message.getmessage(event_data)
    
    if event_data.get('message_type') == "group":
        log.logger.info(f"[BotCore] GroupMessage in {event_data.get('group_id')} {event_data.get('sender').get('nickname')}:{processed_message.msg}")
    if event_data.get('message_type') == "private":
        log.logger.info(f"[BotCore] PrivateMessage in {event_data.get('user_id')} {event_data.get('sender').get('nickname')}:{processed_message.msg}")
    
    if await botinfo.main(event_data, api.event, log.logger, login_info):
        return jsonify({'status': 'success', 'message': 'Event received'}), 200
    
    try:
        await plugin.work(processed_message, api.event)
    except Exception as e:
        #print(e)
        pass


    #log.logger.info(str(event_data))  #debug


    return jsonify({'status': 'success', 'message': 'Event received'}), 200


if __name__ == '__main__':
    host = '127.0.0.1'
    port = '5000'
    listener.run(host=host, port=port)