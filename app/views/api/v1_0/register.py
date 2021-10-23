# -*- encoding: utf-8 -*-
"""
@File Name      :   register.py    
@Create Time    :   2021/7/14 21:38
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

from flask import Blueprint, request, current_app

from app.libs.enums import ClientTypeEnum
from app.libs.error_exception import Success, ParameterException, LinkError
from app.utils.wtf_handler.client import ClientForm
from app.utils.wtf_handler.register import RegisterOnlyUsernameForm, RegisterEmailForm, RegisterPhoneForm, \
    RegisterEmailWithUsernameForm
from app.viewModels.common.verification import verify_verification_code,send_verification_code_full
from app.viewModels.tcm.register import (
    register_user_by_email, register_user_by_phone, register_user_by_username,
    confirm_register_link
)

register_bp = Blueprint('register', __name__)


def __register_by_username():
    form = RegisterOnlyUsernameForm().validate_for_api()
    return register_user_by_username(form.account.data, form.secret.data)


def __register_by_email():
    form = RegisterEmailForm().validate_for_api()
    return register_user_by_email(form.email.data, form.secret.data, form.account.data)


def __register_by_username_email():
    form = RegisterEmailWithUsernameForm().validate_for_api()
    return register_user_by_email(form.email.data, form.secret.data, form.account.data)


def __register_by_phone():
    form = RegisterPhoneForm().validate_for_api()
    return register_user_by_phone(form.account.data, form.secret.data)


@register_bp.post('/new_user')
def register():
    print(request.get_json())
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_NAME: __register_by_username,
        ClientTypeEnum.USER_EMAIL: __register_by_email,
        ClientTypeEnum.NAME_EMAIL: __register_by_username_email,
        ClientTypeEnum.USER_PHONE: __register_by_phone
    }
    promise[ClientTypeEnum(form.type.data)]()
    return Success()


@register_bp.post('/get_email_register_verification_code')
def get_register_verification_code():
    data = request.get_json()
    email = data.get('email', '')
    if email:
        send_verification_code_full(email, 'register')
        return Success(msg='send success', chinese_msg='验证码发送成功，请查看邮箱')
    else:
        return ParameterException(msg='no email', chinese_msg='没有邮箱，无法发送验证码')


@register_bp.post('/verify_email_register_verification_code')
def email_register_verification_code():
    data = request.get_json()
    email = data.get('email', '')
    code = data.get('verification_code', '')
    if email and code:
        verify_verification_code(code, email, 'register')
        return Success(msg='send success', chinese_msg='验证码发送成功，请查看邮箱')
    else:
        return ParameterException(msg='no email', chinese_msg='没有邮箱或验证码，验证失败')


@register_bp.post('/verify_by_email')
def verify_by_email_by_post():
    data = request.get_json()
    register_link = data.get('register_link', '')
    secret_key = current_app.config['CRYPTOGRAPHY_SECRET_KEY']
    if confirm_register_link(register_link, secret_key):
        return Success(msg='verify success', chinese_msg='验证成功')
    else:
        return LinkError(msg='link invalid', chinese_msg='链接非法或过期')


@register_bp.get('/verify_by_email/<string:register_link>')
def verify_by_email(register_link):
    secret_key = current_app.config['CRYPTOGRAPHY_SECRET_KEY']
    if confirm_register_link(register_link, secret_key):
        return Success(msg='verify success', chinese_msg='验证成功')
    else:
        return LinkError(msg='link invalid', chinese_msg='链接非法或过期')
