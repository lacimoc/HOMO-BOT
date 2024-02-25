# -*- coding: utf-8 -*-

import logging
import os
import datetime

if not os.path.exists(f'{os.getcwd()}\\log'):
    os.makedirs(f'{os.getcwd()}\\log\\')

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

log_file = f'{os.getcwd()}\\log\\{datetime.date.today().strftime("%Y-%m-%d")}.log'  # 日志文件路径
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

logger.addHandler(console_handler)
logger.addHandler(file_handler)