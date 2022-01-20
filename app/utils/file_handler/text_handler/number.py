# -*- encoding: utf-8 -*-
"""
@File Name      :   number.py    
@Create Time    :   2022/1/15 14:51
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'


def int_to_bin(num: int):
    """
    Python的二进制是倒过来的，需要把前面的'0b'去掉再取反
    """
    return bin(num)[2:][::-1]
