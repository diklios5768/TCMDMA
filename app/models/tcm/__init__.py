# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py    
@Create Time    :   2021/12/4 15:35
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

from app.models.base_models.base import Base
from app.models.base_models.management import BaseLog
from app.models.base_models.user import BaseUser, BaseRole

many_to_many_table_base_info = {'bind_key': 'users'}


class TCM:
    __abstract__ = True
    __bind_key__ = 'tcm_dma'


class TCMBase(TCM, Base):
    pass


class TCMBaseUser(TCM, BaseUser):
    pass


class TCMBaseRole(TCM, BaseRole):
    pass


class TCMBaseLog(TCM, BaseLog):
    pass
