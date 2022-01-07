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

from datetime import datetime, timedelta


def generate_datetime_str_now(str_format='%Y-%m-%d-%H-%M-%S'):
    return str(datetime.utcnow().strftime(str_format))


def generate_datetime_timestamp_now():
    return datetime.utcnow().timestamp()


def generate_datetime_str_from_timestamp(timestamp, str_format='%Y-%m-%d-%H-%M-%S'):
    return str(datetime.fromtimestamp(float(timestamp)).strftime(str_format))


def generate_datetime_timestamp_from_str(datetime_str, str_format='%Y-%m-%d-%H-%M-%S'):
    return datetime.strptime(datetime_str, str_format).timestamp()


def generate_celery_delay_time(seconds):
    return datetime.utcnow() + timedelta(seconds=seconds)


def _get_duration_components(duration):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds


def duration_iso_string(duration):
    if duration < timedelta(0):
        sign = '-'
        duration *= -1
    else:
        sign = ''

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = '.{:06d}'.format(microseconds) if microseconds else ""
    return '{}P{}DT{:02d}H{:02d}M{:02d}{}S'.format(sign, days, hours, minutes, seconds, ms)
