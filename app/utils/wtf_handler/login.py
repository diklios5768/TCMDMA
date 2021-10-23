# -*- encoding: utf-8 -*-
"""
@File Name      :   login.py    
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

from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from app.models.tcm.user import User
from app.utils.wtf_handler.client import ClientForm, RememberForm, ExtraVerificationCodeForm
from app.viewModels.common.verification import verify_verification_code


# 用户名+密码
class LoginUsernameForm(RememberForm):
    account = StringField(validators=[DataRequired(), Length(min=4, max=20)])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$',message='secret invalid')])

    def validate_account(self, value):
        if not User.query.filter_by(username=value.data).first():
            raise ValidationError('没有这个账号')


# 邮箱+密码
class LoginEmailForm(RememberForm):
    account = StringField(validators=[DataRequired(), Email(message='invalidate email')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])

    def validate_account(self, value):
        if not User.query.filter_by(email=value.data).first():
            raise ValidationError('没有这个账号')


# 邮箱+验证码
class LoginEmailUseVerificationCodeForm(RememberForm, ExtraVerificationCodeForm):
    def validate_account(self, value):
        if not User.query.filter_by(email=value.data).first():
            raise ValidationError('没有这个账号')

    def validate_verification_code(self, value):
        verify_verification_code(account_type='email', account=self.account.data, verification_code=value.data,
                                 use='login')


# todo:手机区号要查询写入，需要再修改
# 手机号+密码
class LoginPhoneForm(RememberForm):
    # phone_code= StringField(validators=[DataRequired(), Length(min=1, max=4)])
    account = StringField(validators=[DataRequired(), Length(12)])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])

    def validate_account(self, value):
        if not User.query.filter_by(phone=value.data).first():
            raise ValidationError('没有这个账号')


# 手机号+验证码
class LoginPhoneUseVerificationCodeForm(RememberForm, ExtraVerificationCodeForm):
    def validate_account(self, value):
        if not User.query.filter_by(phone=value.data).first():
            raise ValidationError('没有这个账号')

    def validate_verification_code(self, value):
        verify_verification_code(account_type='phone', account=self.account.data, verification_code=value.data,
                                 use='login')
