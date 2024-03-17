# -*- coding: utf-8 -*-

import time
import os

import bot
from bot.flask import Flask, request, jsonify
from bot import api
from bot import log
from bot import botinfo
from bot import message
from bot import botcore


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
    
    #log.logger.info(str(event_data))  #debug
    
    processed_message = message.getmessage(event_data)
    
    if processed_message.notice_type == "group_recall" or processed_message.notice_type == "private_recall":
        log.logger.info(f"[BotCore] {processed_message.notice_type[:-7]}_recall Operator_id: {processed_message.operator_id} Messageid: {processed_message.msg_id}")
    if event_data.get('message_type') == "group":
        log.logger.info(f"[BotCore] GroupMessage in {event_data.get('group_id')} {event_data.get('sender').get('nickname')}:{processed_message.msg}")
    if event_data.get('message_type') == "private":
        log.logger.info(f"[BotCore] PrivateMessage in {event_data.get('user_id')} {event_data.get('sender').get('nickname')}:{processed_message.msg}")

    if await botcore.bot_core_event(processed_message, api.event):
        return jsonify({'status': 'success', 'message': 'Event received'}), 200
    
    if await botinfo.main(processed_message, api.event, log.logger, login_info):
        return jsonify({'status': 'success', 'message': 'Event received'}), 200
    
    await plugin.work(processed_message, api.event)

    return jsonify({'status': 'success', 'message': 'Event received'}), 200


if __name__ == '__main__':
    host = '127.0.0.1'
    try:
        with open(file=os.getcwd()+"\\conf\\config.json", mode='r') as conf:
            import json
            port = json.load(conf).get('report_port')
            if port == None:
                raise FileNotFoundError
    except FileNotFoundError:
        with open(file=os.getcwd()+"\\conf\\config.json", mode='w') as conf:
            import json
            json.dump({"report_port":"","listen_port":""})
            raise FileNotFoundError
    listener.run(host=host, port=port)
