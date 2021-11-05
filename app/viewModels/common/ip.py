# -*- encoding: utf-8 -*-
"""
@File Name      :   ip.py    
@Create Time    :   2021/11/4 13:59
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

from app.models import redis


def init_banned_ip_address():
    redis.sadd('banned_ip_address', 'init')


def add_banned_ip_address(ip):
    try:
        redis.sadd('banned_ip_address', ip)
        return True
    except Exception as e:
        print(e)
        return False


def get_banned_ip_addresses():
    return redis.smembers('banned_ip_address')


def is_banned_ip_address(token):
    return redis.sismember('banned_ip_address', token)


def remove_banned_ip_address(token):
    return redis.srem('banned_ip_address', token)
