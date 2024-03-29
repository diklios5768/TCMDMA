# -*- encoding: utf-8 -*-
"""
@File Name      :   development.py    
@Create Time    :   2021/10/8 17:17
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

from .user import init_role, init_user
from .analysis import init_method, update_method


def init_development_data():
    init_role()
    init_user()
    init_method()


def update_development_data():
    update_method()
