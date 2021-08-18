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

from flask import Blueprint, request
from app.libs.enums import ClientTypeEnum
from app.libs.error_exception import Success
from app.utils.wtf_handler.client import ClientForm
from app.utils.wtf_handler.register import RegisterOnlyUsernameForm, RegisterEmailForm, RegisterPhoneForm, \
    RegisterEmailWithUsernameForm
from app.viewModels.tcm.register import register_user_by_email, register_user_by_phone, register_user_by_username

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
