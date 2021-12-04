# -*- encoding: utf-8 -*-
"""
@File Name      :   sqlalchemy.py    
@Create Time    :   2021/7/12 15:53
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

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from contextlib import contextmanager
from app.libs.error_exception import CommitFailed


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
            raise CommitFailed(msg=str(e))
