# -*- encoding: utf-8 -*-
"""
@File Name      :   register.py    
@Create Time    :   2021/7/14 20:44
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

from app.libs.error_exception import ParameterException
from app.models import db
from app.models.tcm.user import User,Role

from app.utils.random import random_content


# 注册
# 用用户名和密码注册，两种都是必须
def register_user_by_username(username, password):
    role_user = Role.query.filter_by(id=1).first_or_404()
    with db.auto_commit():
        user = User()
        user.set_attrs({'username': username})
        user.set_password(password)
        user.roles.append(role_user)
        db.session.add(user)


# 邮箱注册不仅需要邮箱和密码，还可以加上用户名
def register_user_by_email(email, password, username=None):
    role_user = Role.query.filter_by(id=1).first_or_404()
    with db.auto_commit():
        user = User()
        user.set_attrs({'email': email})
        user.set_password(password)
        if username is not None:
            user.set_attrs({'username': username})
        user.roles.append(role_user)
        db.session.add(user)


# 手机注册可以只使用验证码，密码不是必须，给出默认随机密码当做当前密码，只能通过手机验证码修改
# 可以同时要求加上密码
# 也可以加上用户名，但是无法用于登录
def register_user_by_phone(phone, password=None, username=None):
    role_user = Role.query.filter_by(id=1).first_or_404()
    with db.auto_commit():
        user = User()
        user.set_attrs({'phone': phone})
        if password is not None:
            user.set_password(password)
        else:
            user.set_password(random_content(length=16, random_type='password'))
        if username is not None:
            user.set_attrs({'username': username})
        user.roles.append(role_user)
        db.session.add(user)
