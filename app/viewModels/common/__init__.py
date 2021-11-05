# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py    
@Create Time    :   2021/11/4 14:17
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

from app.viewModels.common.token import init_banned_token
from app.viewModels.common.ip import init_banned_ip_address

def init_redis_production():
    init_banned_token()
    init_banned_ip_address()

def init_redis_development():
    init_redis_production()