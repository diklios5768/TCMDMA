# -*- encoding: utf-8 -*-
"""
@File Name      :   captcha.py    
@Create Time    :   2021/7/14 22:07
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

from flask import current_app

from app.libs.error_exception import CaptchaError, \
    CaptchaOutOfDateError
from app.models import redis
from app.utils.celery_handler import celery
from app.utils.mail_handler.login_register import send_captcha_mail
from app.utils.random import random_content
from app.utils.time import generate_celery_delay_time, generate_datetime_timestamp_now


# 使用redis数据库管理验证码
def generate_captcha(identification, use='register'):
    captcha = str(random_content(6, 'number'))
    captcha_content = str(identification) + '--' + str(use) + '--' + str(generate_datetime_timestamp_now())
    redis.set(captcha, captcha_content)
    return captcha


def verify_captcha(code, identification, use='register'):
    captcha_content = redis.get(code)
    if captcha_content:
        content_identification, content_use, content_timestamp = captcha_content.split('--')
        timestamp_now = generate_datetime_timestamp_now()
        timestamp_expiration = float(content_timestamp) + float(current_app.config['CAPTCHA_EXPIRATION'])
        if str(identification) == content_identification and str(use) == content_use:
            if timestamp_now <= timestamp_expiration:
                redis.delete(code)
                return True
            else:
                raise CaptchaOutOfDateError()
        else:
            raise CaptchaError()
    else:
        raise CaptchaOutOfDateError()


@celery.task(shared=False)
def delete_captcha(code):
    redis.delete(code)
    return True


# 发送验证码完整流程
def send_captcha_full(email, use):
    code = generate_captcha(email, use)
    send_captcha_mail.delay(code, email)
    try:
        delete_captcha.apply_async(args=(code,), eta=generate_celery_delay_time(
            current_app.config['CAPTCHA_EXPIRATION']))
    except Exception as e:
        print(str(e))
