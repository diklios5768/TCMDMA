# -*- encoding: utf-8 -*-
"""
@File Name      :   login.py    
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

from datetime import datetime

from flask import Blueprint, current_app, jsonify, request, g

from app.libs.enums import ClientTypeEnum
from app.libs.error_exception import Success, LoginSuccess, AuthFailed, ParameterException, Forbidden
from app.models.tcm.user import User
from app.utils.token_auth import auth
from app.utils.token_auth import generate_auth_token, get_token_info
from app.utils.wtf_handler.client import ClientForm
from app.utils.wtf_handler.login import LoginUsernameForm, LoginEmailForm, LoginPhoneForm, \
    LoginEmailUserCaptchaForm, LoginPhoneUserCaptchaForm
from app.viewModels import database_read_by_id_single
from app.viewModels.common.token import ban_token
from app.viewModels.tcm.login import verify_user

login_bp = Blueprint('login', __name__)


def __login_by_username():
    form = LoginUsernameForm().validate_for_api()
    return verify_user('username', form.account.data, form.secret.data)


def __login_by_email():
    form = LoginEmailForm().validate_for_api()
    return verify_user('email', form.account.data, form.secret.data)


def __login_by_email_with_captcha():
    form = LoginEmailUserCaptchaForm().validate_for_api()
    return verify_user('email', form.account.data)


def __login_by_phone():
    form = LoginPhoneForm().validate_for_api()
    return verify_user('phone', form.account.data, form.secret.data)


def __login_by_phone_with_captcha():
    form = LoginPhoneUserCaptchaForm().validate_for_api()
    return verify_user('phone', form.account.data)


@login_bp.post('')
def login():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_NAME: __login_by_username,
        ClientTypeEnum.USER_EMAIL: __login_by_email,
        ClientTypeEnum.USER_PHONE: __login_by_phone
    }
    identity = promise[ClientTypeEnum(form.type.data)]()
    # 生成Token
    refresh_token_expiration = current_app.config['REFRESH_TOKEN_EXPIRATION']
    refresh_token = generate_auth_token(identity['uid'], form.type.data.value, identity['scopes'],
                                        refresh_token_expiration, 'refresh')
    access_token_expiration = current_app.config['ACCESS_TOKEN_EXPIRATION']
    access_token = generate_auth_token(identity['uid'], form.type.data.value, identity['scopes'],
                                       access_token_expiration, 'access')
    t = {
        "data": {
            'access_token': access_token.decode('ascii')
        }
    }
    res = jsonify(t)
    # cookie不设置expires的话过期时间是游览器会话结束
    # max_age单位是秒，从现在开始计算
    # expires单位是时间戳，可以使用datetime创建，如果设置的是数字，则从1970年1月1号开始算
    res.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=False,
                   expires=datetime.utcnow().timestamp() + refresh_token_expiration)
    return res


@login_bp.get('/current_user')
@auth.login_required
def is_login():
    token_info = g.token_info
    user = database_read_by_id_single(class_id=token_info.uid, database_class=User)
    current_user = dict(user)
    # 暂时不直接返回权限等级，方便使用
    current_user['user_admin'] = False
    for role in user.roles:
        if role.access_level >= 80:
            current_user['user_admin'] = True
            break
    return Success(data=current_user)


@login_bp.get('/is_token_valid')
@auth.login_required
def is_token_valid():
    return Success(msg='Token is valid')


@login_bp.get('/get_new_access_token/')
def get_new_access_token():
    refresh_token = request.cookies.get('refresh_token', None)
    if refresh_token is not None:
        token_info = get_token_info(refresh_token)
        if token_info['token_use'] != 'refresh':
            raise Forbidden(msg='token use error', chinese_msg='token的用途错误')
        access_token = generate_auth_token(token_info['uid'], token_info['client_type'], token_info['scopes'],
                                           'access')
        t = {
            'access_token': access_token.decode('ascii')
        }
        return LoginSuccess(data=t)
    else:
        return AuthFailed()


@login_bp.get('/logout')
def logout():
    # refresh_token放入黑名单,access_token时间非常短，可以不放
    refresh_token = request.cookies.get('refresh_token', None)
    if refresh_token:
        token_info = get_token_info(refresh_token)
        if token_info['token_use'] != 'refresh':
            raise Forbidden(msg='token use error', chinese_msg='token的用途错误')
        ban_token(refresh_token, token_info['expire_in'] - int(datetime.utcnow().timestamp()))
        # 登出
        res = jsonify({'success': True, 'msg': 'logout success'})
        res.delete_cookie('refresh_token')
        return res
    else:
        return ParameterException(msg='cookies has no token', chinese_msg='cookies中没有token')
