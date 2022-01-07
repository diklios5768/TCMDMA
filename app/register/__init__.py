# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/11/2 8:39
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

import dataclasses
import datetime
import decimal
import uuid

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_exception import ServerError
from app.utils.time import duration_iso_string


# 需要重写Flask和JSONEncoder，从而解决jsonify序列化对象的问题
class JSONEncoder(_JSONEncoder):
    # 实际上default是递归调用的
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime("%a, %d %b %Y %H:%M:%S GMT")
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if o.utcoffset() is not None:
                raise ServerError(msg="JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        else:
            return super(JSONEncoder, self).default(o)



class Flask(_Flask):
    json_encoder = JSONEncoder
