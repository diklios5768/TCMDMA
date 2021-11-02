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

import logging
import os
import time
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import request

from app.settings import basedir
from app.utils.file_handler import make_dir


# log配置，实现日志自动按日期生成日志文件
def create_file_log_handler():
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
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # 将日志记录器指定日志的格式
    file_log_handler.setFormatter(formatter)
    # 日志等级的设置
    file_log_handler.setLevel(logging.INFO)
    return file_log_handler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super(RequestFormatter, self).format(record)


def create_request_formatter():
    return RequestFormatter(
        '[%asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )


def create_mail_handler():
    mail_handler = SMTPHandler(
        mailhost=os.getenv('MAIL_SERVER'),
        fromaddr=os.getenv('MAIL_USERNAME'),
        toaddrs=os.getenv('ADMIN_MAIL'),
        subject='Application Error',
        credentials=(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(create_request_formatter())


# 日志系统配置
def register_logger(app):
    app.logger.setLevel(logging.INFO)
    # 一般的日志保存在本地
    app.logger.addHandler(create_file_log_handler())
    # 错误日志发送到邮件
    app.logger.addHandler(create_mail_handler())
    # 某些云平台可能需要SteamHandler
    # from flask.logging import default_handler
    # default_handler.setLevel(logging.INFO)
    # app.logger.addHandler(default_handler)
