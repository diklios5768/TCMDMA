# -*- encoding: utf-8 -*-
"""
@File Name      :   token.py    
@Create Time    :   2021/10/23 8:54
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
from app.utils.celery_handler import celery
from app.utils.time import generate_celery_delay_time


def init_banned_token():
    redis.sadd('banned_token', 'init')


def add_banned_token(token):
    try:
        redis.sadd('banned_token', token)
        return True
    except Exception as e:
        print(e)
        return False


def get_banned_token():
    return redis.smembers('banned_token')


def is_banned_token(token):
    return redis.sismember('banned_token', token)


@celery.task(shared=False)
def remove_banned_token(token):
    return redis.srem('banned_token', token)


def ban_token(token, expiration):
    add_banned_token(token)
    remove_banned_token.apply_async(args=(token,), eta=generate_celery_delay_time(expiration))
