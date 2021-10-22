# -*- encoding: utf-8 -*-
"""
@File Name      :   verification.py    
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

from datetime import datetime
from flask import current_app
from app.libs.error_exception import SendEmailSuccess, SendPhoneSuccess, NotFound, VerificationCodeError, \
    VerificationCodeOutOfDateError, ParameterException
from app.models import db
from app.models.common.verification import EmailVerification, PhoneVerification
from app.utils.random import random_content
from app.utils.time import generate_celery_delay_time
from app.utils.file_handler.text_handler.verification_code import generate_verification_code
from app.utils.celery_handler.mail import send_verification_code_mail_sync
from app.utils.celery_handler.verification_code import delete_verification_code_sync


def search_verification(account_type, account, verification_code):
    try:
        if account_type == 'email':
            verification = EmailVerification.query.filter_by(email=account,
                                                             verification_code=verification_code).first_or_404()
        elif account_type == 'phone':
            verification = PhoneVerification.query.filter_by(phone=account,
                                                             verification_code=verification_code).first_or_404()
        else:
            raise ParameterException()
    except NotFound:
        raise VerificationCodeError()
    return verification


def send_verification_code_to_email(email, verification_time=None, use=None):
    with db.auto_commit():
        random_verification_code = random_content(length=6, type='verification_code')
        if verification_time is not None:
            expiration = verification_time
        else:
            expiration = current_app.config['VERIFICATION_TIME']
        if use is not None:
            use = use
        else:
            use = 'register'
        verification = EmailVerification()
        verification.set_attrs(
            {'email': email, 'verification_code': random_verification_code, 'expiration': expiration, 'use': use})
        db.session.add(verification)
    # todo:数据库提交成功后发送验证码到邮件，如果验证码发送成功，返回SendEmailSuccess
    return True


def send_verification_code_to_phone(phone, verification_time=None, use=None):
    with db.auto_commit():
        random_verification_code = random_content(length=6, type='verification_code')
        if verification_time is not None:
            expiration = verification_time
        else:
            expiration = current_app.config['VERIFICATION_TIME']
        if use is not None:
            use = use
        else:
            use = 'register'
        verification = PhoneVerification()
        verification.set_attrs(
            {'phone': phone, 'verification_code': random_verification_code, 'expiration': expiration, 'use': use})
        db.session.add(verification)
    # todo:数据库提交成功后发送验证码到手机，如果验证码发送成功，返回SendPhoneSuccess
    return True


def verify_verification_code(account_type, account, verification_code, use='register'):
    verification = search_verification(account_type, account, verification_code)
    if verification.expiration + verification.create_date <= datetime.utcnow().timestamp():
        raise VerificationCodeOutOfDateError()
    if verification.use == use:
        return True
    else:
        raise VerificationCodeError()


# 手动失效
def disable_verification_code(account_type, account, verification_code):
    with db.auto_commit():
        verification = search_verification(account_type, account, verification_code)
        verification.valid = False


# 使用redis数据库管理验证码
# 发送验证码完整流程
def send_verification_code_full(email, use):
    code = generate_verification_code(email, use)
    send_verification_code_mail_sync.delay(code, email)
    try:
        delete_verification_code_sync.apply_async(args=(code,), eta=generate_celery_delay_time(
            current_app.config['VERIFICATION_TIME']))
    except Exception as e:
        print(str(e))
