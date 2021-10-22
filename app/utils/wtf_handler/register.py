# -*- encoding: utf-8 -*-
"""
@File Name      :   register.py    
@Create Time    :   2021/7/15 10:04
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

from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp
from app.models.tcm.user import User
from app.utils.wtf_handler.client import ClientForm, ExtraUsernameForm, VerifySecretForm, ExtraVerificationCodeForm


# 用户名+密码
class RegisterOnlyUsernameForm(VerifySecretForm):
    account = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_]{8,20}$', message='用户名不合法，只能包含英文字母、数字和下划线'),
                                      Length(min=4, max=20, message='用户名长度不正确')])

    def validate_account(self, value):
        if User.query.filter_by(username=value.data).first():
            raise ValidationError('用户名已经被注册')


# 邮箱+密码
class RegisterEmailForm(VerifySecretForm):
    account = StringField(validators=[DataRequired(), Email(message='invalidate email')])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('邮箱已经被注册')


# 邮箱+密码+验证码
class RegisterEmailWithSecretForm(RegisterEmailForm, ExtraVerificationCodeForm):
    pass


# 邮箱+密码+用户名
class RegisterEmailWithUsernameForm(VerifySecretForm):
    account = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_]{8,20}$', message='用户名不合法，只能包含英文字母、数字和下划线'),
                                      Length(min=4, max=20, message='用户名长度不正确')])
    email = StringField(validators=[DataRequired(), Email(message='invalidate email')])

    def validate_account(self, value):
        if User.query.filter_by(username=value.data).first():
            raise ValidationError('用户名已经被注册')

    def validate_email(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('邮箱已经被注册')


# 邮箱+密码+验证码+用户名
class RegisterEmailWithUsernameWithSecretForm(RegisterEmailWithUsernameForm, ExtraVerificationCodeForm):
    pass


# todo:手机区号要查询写入，需要再修改
# 手机号+验证码
class RegisterPhoneForm(ClientForm, ExtraVerificationCodeForm):
    # phone_code= StringField(validators=[DataRequired(), Length(min=1, max=4)])
    account = StringField(
        validators=[DataRequired(), Regexp(r'^[0-9]{8,13}$', message='用户名不合法，只能包含英文字母、数字和下划线'), Length(8, 13)])

    def validate_account(self, value):
        if User.query.filter_by(phone=value.data).first():
            raise ValidationError('手机号已经被注册')


# 手机号+验证码+密码
class RegisterPhoneWithSecretForm(RegisterPhoneForm, VerifySecretForm):
    pass


# 手机号+验证码+用户名
class RegisterPhoneWithUsernameForm(RegisterPhoneForm, ExtraUsernameForm):
    pass


# 手机号+验证码+密码+用户名
class RegisterPhoneWithSecretWithUsernameForm(RegisterPhoneWithSecretForm, ExtraUsernameForm):
    pass
