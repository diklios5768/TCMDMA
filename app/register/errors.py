# -*- encoding: utf-8 -*-
"""
@File Name      :   errors.py    
@Create Time    :   2021/11/2 8:41
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
from flask import redirect,url_for
from werkzeug.exceptions import HTTPException

from app.libs.error import APIException
from app.libs.error_exception import ServerError,APILimited,NotFound


# 注册错误处理函数
def register_errors(app):
    # 1.0以后才能捕捉到所有的异常（包括abort()），返回格式改为通用的格式
    # 注意这里只捕捉了异常，成功的并不会被捕捉
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 999
            return APIException(success=False, code=code, error_code=error_code, msg=msg)
        elif isinstance(e,TypeError):
            return ServerError(msg=str(e))
        else:
            # 调试模式的时候显示错误信息
            if not app.config['DEBUG']:
                return ServerError()
            else:
                raise e

    @app.errorhandler(429)
    def rate_limit_handler(e):
        return APILimited(msg=e.description)

    @app.errorhandler(404)
    def not_found_handler(e):
        return redirect(url_for('main.not_found'))
