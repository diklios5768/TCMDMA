# -*- encoding: utf-8 -*-
"""
@File Name      :   login.py    
@Create Time    :   2021/7/14 20:45
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

from app.libs.error_exception import AuthFailed, ParameterException, AccountBannedError, AccountNotConfirmedError
from app.models import db
from app.models.tcm.user import User


def verify_user(verify_type, account, password=None):
    if verify_type == 'username':
        user = User.query.filter_by(username=account).first_or_404()
    elif verify_type == 'email':
        user = User.query.filter_by(email=account).first_or_404()
    elif verify_type == 'phone':
        user = User.query.filter_by(phone=account).first_or_404()
    else:
        raise ParameterException()
    if not user.active:
        raise AccountBannedError()
    if not user.confirmed:
        raise AccountNotConfirmedError()
    if password is not None:
        if not user.validate_password(password):
            raise AuthFailed(msg='password error', chinese_msg='密码错误')
        else:
            with db.auto_commit():
                user.touch()
            return get_user_info(user)
    else:
        raise AuthFailed(msg='password is null', chinese_msg='密码为空')


def get_user_info(user: User):
    scopes = []
    roles = user.roles
    for role in roles:
        if role.access_level >= 1:
            scopes.append('UserScope')
        if role.access_level >= 80:
            scopes.append('AdminScope')
        if role.access_level >= 100:
            scopes.append('SuperAdminScope')
    return {'uid': user.id, 'scopes': scopes}
