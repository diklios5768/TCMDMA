# -*- encoding: utf-8 -*-
"""
@File Name      :   time.py    
@Create Time    :   2021/8/2 11:01
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

from datetime import datetime


def generate_datetime_str_now(str_format='%Y-%m-%d-%H-%M-%S'):
    return str(datetime.utcnow().strftime(str_format))


def generate_datetime_timestamp_now():
    return datetime.utcnow().timestamp()


def generate_datetime_str_from_timestamp(timestamp, str_format='%Y-%m-%d-%H-%M-%S'):
    return str(datetime.fromtimestamp(float(timestamp)).strftime(str_format))


def generate_datetime_timestamp_from_str(datetime_str, str_format='%Y-%m-%d-%H-%M-%S'):
    return datetime.strptime(datetime_str, str_format).timestamp()
