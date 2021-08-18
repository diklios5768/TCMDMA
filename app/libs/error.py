import json

from flask import request
from werkzeug.exceptions import HTTPException


# 通常用于已知异常
class APIException(HTTPException):
    """
    attention:常用HTTP状态码请查看code.md
    """
    # 默认错误码
    code = 500
    success = False
    data = None
    error_code = 999
    msg = ''
    chinese_msg = ''

    def __init__(self, code=None, success=None, data=None, error_code=None, msg=None, chinese_msg=None, headers=None):
        if code:
            self.code = code
        if success:
            self.success = success
        if data:
            self.data = data
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if chinese_msg:
            self.chinese_msg = chinese_msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            success=self.success,
            data=self.data,
            error_code=self.error_code,
            msg=self.msg,
            chinese_msg=self.chinese_msg,
            request=request.method + ' ' + self.get_url_no_param(),
            host=request.remote_addr,
            user_agent=str(request.user_agent)
        )
        text = json.dumps(body)
        return text

    # 强制只使用JSON传递数据
    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json')]

    # 无问号后面参数的的url
    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
