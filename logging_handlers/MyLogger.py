#coding:utf-8
#日志管理类, wrote by tzf, 2018/5/11
import os
import time
import logging.config
import json

def setup_logging(
        default_path='logging_handlers/logging.json',
        default_level=logging.DEBUG,
        env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

class MyLogger(object):

    def __init__(self):
        pass

    def mylogger(self):
        # if level == 'debug':
        #     logging_level = logging.DEBUG
        # elif level == 'info':
        #     logging_level = logging.INFO
        # elif level == 'warning':
        #     logging_level = logging.WARNING
        # elif level == 'error':
        #     logging_level = logging.ERROR
        # else:
        #     logging_level = logging.CRITICAL
        setup_logging()
        logger = logging.getLogger(__name__)
        return logger


'''
   日志系统，日志输出到控制台以及写入日志文件中
   loggname - 日志文件名称
   loglevel - 日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）
'''
# class MyLogger():
#
#     def __init__(self, logname, loglevel, logger):
#         '''
#            指定保存日志的文件路径，日志级别，以及调用文件
#            将日志存入到指定的文件中
#         '''
#
#         # 创建一个logger
#         self.logger = logging.getLogger(logger)
#         self.logger.setLevel(logging.DEBUG)
#
#         # 创建一个handler，用于写入日志文件
#         fh = logging.FileHandler(logname)
#         fh.setLevel(logging.DEBUG)
#
#         # 再创建一个handler，用于输出到控制台
#         ch = logging.StreamHandler()
#         ch.setLevel(logging.DEBUG)
#
#         # 定义handler的输出格式
#         # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         formatter = format_dict[int(loglevel)]
#         fh.setFormatter(formatter)
#         ch.setFormatter(formatter)
#
#         # 给logger添加handler
#         self.logger.addHandler(fh)
#         self.logger.addHandler(ch)
#
#     def getlog(self):
#         return self.logger
#
# #用字典保存日志级别
# format_dict = {
#    1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
#    2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
#    3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
#    4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
#    5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# }