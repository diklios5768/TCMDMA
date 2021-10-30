# -*- encoding: utf-8 -*-
"""
@File Name      :   error_exception.py
@Create Time    :   2021/7/12 11:21
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

from app.libs.error import APIException


# 成功
class Success(APIException):
    code = 200
    success = True
    error_code = 0
    msg = 'success'
    chinese_msg = '成功'


class ReadSuccess(Success):
    error_code = 10
    msg = 'read success'
    chinese_msg = '查询成功'


class CreateSuccess(Success):
    code = 201
    error_code = 11
    msg = 'create success'
    chinese_msg = '创建成功'


class UpdateSuccess(Success):
    code = 201
    error_code = 12
    msg = 'update success'
    chinese_msg = '更新成功'


class TrueDeleteSuccess(Success):
    # attention:code=204的话，即使后端返回了数据，前端也一样不会接受到，因为规范规定了204就是什么都没有，所以可以改为202
    code = 202
    error_code = 13
    msg = 'true delete success'
    chinese_msg = '真删除成功'


class RegisterSuccess(Success):
    error_code = 31
    msg = 'register success'
    chinese_msg = '注册成功'


class LoginSuccess(Success):
    code = 201
    error_code = 32
    msg = 'login success'
    chinese_msg = '登录成功'


class LogoutSuccess(Success):
    error_code = 33
    msg = 'logout success'
    chinese_msg = '退出登录成功'


class AlgorithmAnalysisSuccess(Success):
    error_code = 40
    msg = 'algorithm analysis success'
    chinese_msg = '算法分析成功'


class SendEmailSuccess(Success):
    error_code = 51
    msg = 'send email success'
    chinese_msg = '发送邮件成功'


class SendPhoneSuccess(Success):
    error_code = 52
    msg = 'send phone success'
    chinese_msg = '发送手机短信成功'


class TaskRunningSuccess(Success):
    code = 202
    error_code = 53
    msg = 'task start running'
    chinese_msg = '任务开始执行'


# 失败
class UnknownError(APIException):
    error_code = 999
    msg = 'unknown error'
    chinese_msg = '未知错误'


# 数据错误
class ParameterException(APIException):
    code = 400
    error_code = 1000
    msg = 'invalid parameter'
    chinese_msg = '非法参数'


class NoDataError(ParameterException):
    error_code = 1001
    msg = 'data is None'
    chinese_msg = '关键数据为空'


class DataFormatError(ParameterException):
    error_code = 1002
    msg = 'data type error'
    chinese_msg = '数据格式错误'


class NotFound(APIException):
    code = 404
    error_code = 1010
    msg = 'resources not found'
    chinese_msg = '资源未找到'


# 客户端错误
# 可以使用WTForms内置的ValidationError代替
# 这是给其他没有使用WTForms的表单验证错误时使用
class FormValidateError(APIException):
    code = 400
    error_code = 1300
    msg = 'form validate error'
    chinese_msg = '表单验证失败'


class CaptchaError(FormValidateError):
    error_code = 1301
    msg = 'verification code wrong'
    chinese_msg = '验证码错误'


class CaptchaOutOfDateError(FormValidateError):
    error_code = 1302
    msg = 'verification code out of date'
    chinese_msg = '验证码过期'


class ClientTypeError(FormValidateError):
    error_code = 1303
    msg = "client is invalid"
    chinese_msg = "客户端非法"


class AuthFailed(APIException):
    code = 401
    error_code = 1310
    msg = 'authorization failed'
    chinese_msg = '授权失败'


class TokenInvalid(AuthFailed):
    error_code = 1311
    msg = 'token is invalid'
    chinese_msg = 'token 非法'


class TokenExpired(AuthFailed):
    error_code = 1312
    msg = 'token is expired'
    chinese_msg = 'token 过期'


class TokenDisabled(AuthFailed):
    error_code = 1313
    msg = 'token is disabled'
    chinese_msg = 'token 失效'


class Forbidden(APIException):
    # 禁止访问，并非账号密码错误之类的
    code = 403
    error_code = 1314
    msg = 'forbidden,not in scope'
    chinese_msg = '权限不足'


class LinkError(AuthFailed):
    error_code = 1315
    msg = 'link not exist or verify failed(invalid)'
    chinese_msg = '链接失效或者验证失败（非法）'


# 账户错误
class AccountError(Forbidden):
    error_code = 1320
    msg = 'account error'
    chinese_msg = '账户错误'


class AccountBannedError(AccountError):
    error_code = 1321
    msg = 'account banned'
    chinese_msg = '账户被停用'


class AccountNotConfirmedError(AccountError):
    error_code = 1322
    msg = 'account not confirmed'
    chinese_msg = '账户还未通过'


# 服务器错误
class ServerError(APIException):
    code = 500
    error_code = 1500
    msg = 'sorry,we made a mistake'
    chinese_msg = '服务器发生错误'


# 数据库提交错误
class CommitFailed(ServerError):
    error_code = 1101
    msg = 'database commit failed'
    chinese_msg = '数据库提交失败'


class DatabaseOperationError(ServerError):
    error_code = 1102
    msg = 'database operation method error'
    chinese_msg = '数据库操作错误，无这种操作'
