# -*- coding: utf-8 -*-
# @Time     : 2021/1/7 22:27
# @Author   : qtf
# File      : logger_handler.py

import logging
import logging.handlers
import os
import time
from config.path import logs_path

class LoggerUtil(logging.Logger):
    def __init__(self,
                 name='root',
                 logger_level='DEBUG',
                 stream_handler_level='DEBUG',
                 file_handler_level='INFO',
                 fmt_str="[%(asctime)s] [%(levelname)s] [%(filename)s] [line %(lineno)s] %(message)s"):

        # 获取日志收集器 logger
        super().__init__(name, logger_level)
        # self == 收集器
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.log' % timestamp
        logfilepath = os.path.join(logs_path, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5,
                                                                   encoding='utf-8')
        fmt = logging.Formatter(fmt_str)
        # 日志处理器
        handler = logging.StreamHandler()
        handler.setLevel(stream_handler_level)
        self.addHandler(handler)
        handler.setFormatter(fmt)
        rotatingFileHandler.setFormatter(fmt)
        # 文件处理器
        rotatingFileHandler.setLevel(file_handler_level)
        self.addHandler(rotatingFileHandler)

# if __name__ == '__main__':
#     log = LoggerUtil()
#     log.error("hello 你好!")
logger = LoggerUtil()