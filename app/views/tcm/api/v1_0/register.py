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
from app.utils.file_handler.text_handler.regex import is_email
from app.utils.limiter import register_limit
from app.utils.wtf_handler.client import ClientForm
from app.utils.wtf_handler.register import RegisterOnlyUsernameForm, RegisterEmailForm, RegisterPhoneForm, \
    RegisterEmailWithUsernameWithCaptchaForm
from app.viewModels.common.captcha import verify_captcha, send_captcha_full
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
    return register_user_by_email(form.account.data, form.secret.data, form.username.data)


def __register_by_username_email():
    form = RegisterEmailWithUsernameWithCaptchaForm().validate_for_api()
    return register_user_by_email(form.account.data, form.secret.data, form.username.data)


def __register_by_phone():
    form = RegisterPhoneForm().validate_for_api()
    return register_user_by_phone(form.account.data, form.secret.data)


@register_bp.post('/new_user')
@register_limit
def register():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_NAME: __register_by_username,
        ClientTypeEnum.USER_EMAIL: __register_by_email,
        ClientTypeEnum.NAME_EMAIL: __register_by_username_email,
        ClientTypeEnum.USER_PHONE: __register_by_phone
    }
    promise[ClientTypeEnum(form.type.data)]()
    return Success()


@register_bp.post('/get_email_register_captcha')
@register_limit
def get_email_register_captcha():
    data = request.get_json()
    email = data.get('email', '')
    if is_email(email):
        send_captcha_full(email, 'register')
        return Success(msg='send success', chinese_msg='验证码发送成功，请查看邮箱')
    else:
        return ParameterException(msg='email invalid', chinese_msg='邮箱不合法，无法发送验证码')


@register_bp.post('/verify_email_register_captcha')
def verify_email_register_captcha():
    data = request.get_json()
    email = data.get('email', '')
    code = data.get('captcha', '')
    if is_email(email) and code:
        verify_captcha(code, email, 'register')
        return Success(msg='send success', chinese_msg='验证码发送成功，请查看邮箱')
    else:
        return ParameterException(msg='email or captcha invalid', chinese_msg='邮箱或验证码不合法，验证失败')


@register_bp.post('/verify_by_email_link')
def verify_by_email_link_by_post():
    data = request.get_json()
    register_link = data.get('register_link', '')
    secret_key = current_app.config['CRYPTOGRAPHY_SECRET_KEY']
    if confirm_register_link(register_link, secret_key):
        return Success(msg='verify success', chinese_msg='验证成功')
    else:
        return LinkError(msg='link invalid', chinese_msg='链接非法或过期')


@register_bp.get('/verify_by_email_link/<string:register_link>')
def verify_by_email_link(register_link):
    secret_key = current_app.config['CRYPTOGRAPHY_SECRET_KEY']
    if confirm_register_link(register_link, secret_key):
        return Success(msg='verify success', chinese_msg='验证成功')
    else:
        return LinkError(msg='link invalid', chinese_msg='链接非法或过期')
