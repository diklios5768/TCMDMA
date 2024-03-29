# -*- encoding: utf-8 -*-
"""
@File Name      :   tag.py    
@Create Time    :   2021/7/14 21:06
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

from sqlalchemy import Column, String
from app.models.tcm import TCMBase


class Tag(TCMBase):
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
