# -*- encoding: utf-8 -*-
"""
@File Name      :   verification_code.py    
@Create Time    :   2021/10/22 19:31
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
from app.libs.error_exception import VerificationCodeError,VerificationCodeOutOfDateError
from app.models import redis
from app.utils.random import random_content
from app.utils.time import generate_datetime_timestamp_now


def generate_verification_code(identification, use='register'):
    verification_code = str(random_content(4, 'number'))
    verification_content = str(identification) + '--' + str(use) + '--' + str(generate_datetime_timestamp_now())
    redis.set(verification_code, verification_content)
    return verification_code


def verify_verification_code(code, identification, use='register'):
    verification_content = redis.get(code)
    if verification_content:
        content_identification, content_use, content_timestamp = verification_content.split('--')
        timestamp_now = generate_datetime_timestamp_now()
        timestamp_expiration = float(content_timestamp) + float(current_app.config['VERIFICATION_TIME'])
        if str(identification) == content_identification and str(use) == content_use:
            if timestamp_now <= timestamp_expiration:
                redis.delete(code)
                return True
            else:
                raise VerificationCodeOutOfDateError()
        else:
            raise VerificationCodeError()
    else:
        raise VerificationCodeOutOfDateError()


def delete_verification_code(code):
    redis.delete(code)
