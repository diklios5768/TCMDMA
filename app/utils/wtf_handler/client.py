from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp, EqualTo
from app.libs.enums import ClientTypeEnum
from app.models.tcm.user import User
from app.viewModels.common.captcha import verify_captcha
from app.utils.wtf_handler.base import BaseForm


# 客户端基类


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='不允许为空'), Length(min=2, max=32, message='账户长度不正确')])
    # 类型必须要有，但是密码不一定要有，因为有的客户端没有密码
    # 此处不用PasswordField的原因是数据不一定由表单传入数据，可能是JSON传入数据
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
            self.type.data = client
        except ValueError as e:
            raise e


# 注册的时候验证密码
class VerifySecretForm(ClientForm):
    secret = StringField(
        validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{8,255}$', message='密码不合法'), EqualTo('verify_secret'),
                    Length(8, 255, message='密码长度不正确')])
    verify_secret = StringField('verify_secret', validators=[DataRequired(), Length(8, 255, message='密码长度不正确')])

    def validate_secret(self, value):
        if value.data != self.verify_secret.data:
            raise ValidationError('两次密码输入不一致')


# 登录的时候选择长期登录
class RememberForm(ClientForm):
    remember = BooleanField('Remember me')


# 表单中额外带上用户名
class ExtraUsernameForm(BaseForm):
    username = StringField(
        validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_-]{4,20}$', message='用户名不合法，只能包含英文字母、数字、下划线以及中划线'),
                    Length(min=4, max=20, message='用户名长度不正确')])

    def validate_username(self, value):
        if User.query.filter_by(username=value.data).first():
            raise ValidationError('用户名已经被注册')


# 表单中加上验证码
class ExtraCaptchaForm(BaseForm):
    captcha = StringField(validators=[DataRequired(), Length(min=4, max=8, message='验证码长度不正确')])

    def validate_captcha(self, value):
        verify_captcha(code=value.data, identification=self.account.data, use='register')
