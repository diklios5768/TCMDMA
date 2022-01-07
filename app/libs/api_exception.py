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
    headers = []

    def __init__(self, code: int = 500, success: bool = False, data=None, error_code: int = 999, msg: str = '',
                 chinese_msg: str = '', headers: list[tuple[str, str]] = None):
        self.code = code
        self.success = success
        if data:
            self.data = data
        self.error_code = error_code
        self.msg = msg
        self.chinese_msg = chinese_msg
        if headers:
            self.headers = headers
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            success=self.success,
            data=self.data,
            error_code=self.error_code,
            msg=self.msg,
            chinese_msg=self.chinese_msg,
            request=request.method + ' ' + self.get_url_no_param(),
            remote_addr=request.remote_addr,
            user_agent=str(request.user_agent)
        )
        text = json.dumps(body)
        return text

    # 强制只使用JSON传递数据
    def get_headers(self, environ=None, scope=None) -> list[tuple[str, str]]:
        return [('Content-Type', 'application/json')] + self.headers

    # 无问号后面参数的的url
    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
