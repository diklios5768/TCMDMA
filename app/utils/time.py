# -*- encoding: utf-8 -*-
"""
@File Name      :   time.py    
@Create Time    :   2021/8/2 11:01
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

from datetime import datetime


def generate_datetime_str():
    return str(datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")) + '--'
