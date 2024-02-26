async def group_message(message_data, event): #群组消息时被触发的函数
    #plugin to do
    pass
    #await event.send_group_msg(group_id=message_data['group_id'], data="测试成功") #调用bot.api中的函数发送消息（需要使用await异步）


async def private_message(message_data, event): #私聊消息时被触发的函数
    #plugin to do
    pass
    #await event.send_private_msg(user_id=message_data['user_id'], data="测试成功") #调用bot.api中的函数发送消息（需要使用await异步）
