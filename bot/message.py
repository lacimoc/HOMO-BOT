class PrivateMessage():
        user_id = None
        sender = None
        msg = None
        raw_msg = None
        msg_id = None
        original_message = None
        msg_type = "private"

class GroupMessage():
        group_id = None
        user_id = None
        sender = None
        msg = None
        raw_msg = None
        msg_id = None
        original_message = None
        msg_type = "group"


def getmessage(event_data) -> classmethod:
    if event_data.get('message_type') == 'private':
        class message(PrivateMessage):
            user_id = event_data.get('user_id')
            sender = event_data.get('sender')
            msg = message_to_cq(event_data.get('message'))
            raw_msg = event_data.get('raw_message')
            msg_id = event_data.get('message_id')
            original_message = event_data
            msg_type = event_data.get('message_type')
            operator_id = event_data.get('operator_id')
            notice_type = event_data.get('notice_type')
            sub_type = ""
        return message
    
    if event_data.get('message_type') == 'group':
        class message(GroupMessage):
            group_id = event_data.get('group_id')
            user_id = event_data.get('user_id')
            sender = event_data.get('sender')
            msg = message_to_cq(event_data.get('message'))
            raw_msg = event_data.get('raw_message')
            msg_id = event_data.get('message_id')
            original_message = event_data
            msg_type = event_data.get('message_type')
            operator_id = event_data.get('operator_id')
            notice_type = event_data.get('notice_type')
            sub_type = ""
        return message
    
    if event_data.get('sub_type') != None:
        class message(GroupMessage):
            group_id = event_data.get('group_id')
            user_id = event_data.get('user_id')
            sender = event_data.get('sender')
            msg = message_to_cq(event_data.get('message'))
            raw_msg = event_data.get('raw_message')
            msg_id = event_data.get('message_id')
            original_message = event_data
            msg_type = event_data.get('message_type')
            operator_id = event_data.get('operator_id')
            notice_type = event_data.get('notice_type')
            sub_type = event_data.get('sub_type')
        return message

    if event_data.get('notice_type') != None:
        class message(GroupMessage):
            group_id = event_data.get('group_id')
            user_id = event_data.get('user_id')
            sender = event_data.get('sender')
            msg = ""
            raw_msg = event_data.get('raw_message')
            msg_id = event_data.get('message_id')
            original_message = event_data
            msg_type = event_data.get('message_type')
            operator_id = event_data.get('operator_id')
            notice_type = event_data.get('notice_type')
            sub_type = event_data.get('sub_type')
        return message

def message_to_cq(message) -> str:
    if message == None:
        return " "
    message_len = len(message)
    result = ""
    for i in range(0,message_len):
        try:
            result += encode_to_cq(message[i])
        except TypeError:
            return " "
    return result


def encode_to_cq(message) -> str:
    if message.get('type') == 'text':
        return message.get('data').get('text')
    
    if message.get('type') == 'image':
        return f"[CQ:image,file={message.get('data').get('url')}]"
    
    if message.get('type') == 'record':
        return f"[CQ:record,file={message.get('data').get('file')}]"
    
    if message.get('type') == 'face':
        return f"[CQ:face,id={message.get('data').get('id')}]"
    
    if message.get('type') == 'at':
        return f"[CQ:at,qq={message.get('data').get('qq')}]"

    if message.get('type') == 'reply':
        return f"[CQ:reply,id={message.get('data').get('id')}]"
