# -*- encoding: utf-8 -*-
"""
@File Name      :   logging.py    
@Create Time    :   2021/7/17 14:20
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

import os
import logging
import time
from logging.handlers import RotatingFileHandler
from app.utils.file_handler import make_dir
from app.settings import basedir

# log配置，实现日志自动按日期生成日志文件

# 日志目录名称
log_dir_name = "logs"
# 日志文件名称
log_file_name = 'logs-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
# 日志文件夹路径
log_dir_path = basedir + os.sep + log_dir_name
make_dir(log_dir_path)
# 日志文件路径
log_file_path = log_dir_path + os.sep + log_file_name

# 创建日志记录器，指明日志保存路径，记录到文件，设置每个日志的大小，保存日志的上限
file_log_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=10)
# 设置日志的格式                   发生时间    日志等级     日志信息文件名      函数名          行数        日志信息
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# 将日志记录器指定日志的格式
file_log_handler.setFormatter(formatter)
# 日志等级的设置
file_log_handler.setLevel(logging.DEBUG)

# # 创建日志记录对象
# logger = logging.getLogger()
# # 默认日志等级的设置
# logging.basicConfig(level=logging.DEBUG)
# # 等级： DEBUG < INFO < WARNING < ERROR < CRITICAL
# # DEBUG ： 最详细的日志信息，主要的应用场景问题的诊断，只限于开发人员使用的，用来在开发过程中进行调试
# # INFO ： 详细程度仅次于debug模式，主要来记录关键节点的信息，确定程序是否正常如预期完成，一般的使用场景是重要的业务处理已经结束，我们通过这些INFO级别的日志信息，可以很快的了解应用正在做什么。
# # WARNING ： 当某些不被期望的事情发生的时候，需要记录的信息，比如磁盘即将存满，注意当前的程序一依旧可以正常运行，不报错。也就是说发生这个级别的问题时，处理过程可以继续，但必须要对这个问题给予额外的关注。
# # ERROR ： 出现严重问题，导致某些功能不能正常运行记录信息
# # CRITICAL： 系统即将崩溃或者已经崩溃
# logger.setLevel(logging.DEBUG)
# # 为全局的日志工具对象添加日志记录器
# logger.addHandler(file_log_handler)
#
# # Logging使用
# logger.info("this is info")
# logger.debug("this is debug")
# logger.warning("this is warning")
# logging.error("this is error")
# logger.critical("this is critical")
