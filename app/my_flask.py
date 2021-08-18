# -*- encoding: utf-8 -*-
"""
@File Name      :   app.py
@Create Time    :   2021/7/12 15:09
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

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error_exception import ServerError
from datetime import datetime


# 需要重写Flask和JSONEncoder，从而解决jsonify序列化对象的问题
class JSONEncoder(_JSONEncoder):
    # 实际上default是递归调用的
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        elif isinstance(o, datetime):
            return o.strptime("%a, %d %b %Y %H:%M:%S GMT")
        else:
            raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder
