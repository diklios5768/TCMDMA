# -*- encoding: utf-8 -*-
"""
@File Name      :   query.py
@Create Time    :   2021/7/12 15:35
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

from flask_sqlalchemy import BaseQuery

from app.libs.error_exception import NotFound


# 重写SQLAlchemy的查询类，增加自己的功能
class Query(BaseQuery):
    # 默认增加status的查询，这样就不用在每个地方都写上status=1了，如果原来写上了就是使用写上的，因为可能要查询其他状态
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    # 这样在查询的时候就不需要每个地方都写一个判断存不存在的语句了
    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv
