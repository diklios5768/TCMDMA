# -*- encoding: utf-8 -*-
"""
@File Name      :   reg.py    
@Create Time    :   2021/10/30 17:15
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

import re


def is_email(value: str = ''):
    email_re = re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    result = email_re.match(value)
    if result:
        return True
    else:
        return False
