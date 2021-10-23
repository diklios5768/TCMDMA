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


def add_banned_token(token):
    redis.sadd('banned_token', token)
    return True


def is_banned_token(token):
    return redis.sismember('banned_token', token)


@celery.task(shared=False)
def remove_banned_token(token):
    redis.srem('banned_token', token)
    return True


def ban_token(token, expiration):
    add_banned_token(token)
    remove_banned_token.apply_async(args=(token,), eta=generate_celery_delay_time(expiration))
