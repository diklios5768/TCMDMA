# -*- encoding: utf-8 -*-
"""
@File Name      :   url.py    
@Create Time    :   2021/10/22 16:44
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

from urllib.parse import quote, unquote


# 将中文转换为URL编码格式
def encode_to_url(url):
    return quote(url)


def decode_url(url_encoded):
    return unquote(url_encoded)
