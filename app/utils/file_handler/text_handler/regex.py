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


# 文本分隔符号替换预处理
def replace_character(text):
    return re.sub(r'[，、\t]', ',', re.sub(r'!|！|；|。|\.|\r\n|\r|\n', ';', text))


def replace_row_character(text):
    return re.sub(r'!|！|；|。|\.|\r\n|\r|\n', ';', text)


def replace_col_character(text):
    return re.sub(r'[，、\t]', ',', text)


def is_email(value: str = ''):
    email_re = re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    result = email_re.match(value)
    if result:
        return True
    else:
        return False


def char_index(char, text: str) -> list:
    return [find_char.start() for find_char in re.finditer(char, text)]
