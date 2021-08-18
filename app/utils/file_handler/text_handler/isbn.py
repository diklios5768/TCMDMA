# -*- encoding: utf-8 -*-
"""
@File Name      :   isbn.py    
@Create Time    :   2021/8/9 11:36
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


def is_isbn(text: str):
    # 判断是否是ISBN13
    if len(text) == 13 and text.isdigit():
        return True
    # 判断是否是ISBN10
    short_text = text.replace('-', '')
    if '-' in text and len(short_text) == 10 and short_text.isdigit():
        return True
    else:
        return False
