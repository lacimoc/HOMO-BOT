import os
import sys
import json
import importlib
from bot import log


sys.path.append(__file__[:-15] + "\\app")


class BreakLoop(Exception):  
            pass


class load():
    def get_plugin() -> list:
        file_list = []
        level_dict = {}

        for item in os.listdir(__file__[:-15] + "\\app"):  
            if os.path.isdir(os.path.join(__file__[:-15] + "\\app", item)):
                file_list.append(item)
                with open(file=f"{__file__[:-15]}\\app\\{item}\\level.json", mode='r') as f:
                    level_dict.update(json.load(f))

        level_keys = sorted(level_dict.items(), key=lambda item: item[1])
        level_keys_only = [key for key, value in level_keys] 

        return level_keys_only
    

plugin_list = load.get_plugin()
for i in load.get_plugin():  #插件读入
    try:
        globals()[i] = importlib.import_module(i)
        log.logger.info(f"[plugin_core] {i} 成功被 plugin_core 加载")
    except Exception as e:
        log.logger.error(f"[plugin_core] {i} 由于 **{e}** 被跳过")
        del plugin_list[plugin_list.index(i)]


async def work(message, plugin_event):
    if message.msg_type == 'group':
        for i in plugin_list:
            try:
                try:
                    await globals()[i].main.group_message(message, plugin_event)
                except BreakLoop:
                    pass
            except Exception as e:
                log.logger.warning(f"[plugin_core] {i} raise a error\n{e}")
    if message.msg_type == 'private':
        for i in plugin_list:    
            await globals()[i].main.private_message(message, plugin_event)