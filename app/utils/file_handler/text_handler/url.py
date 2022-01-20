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

from urllib.parse import quote, unquote, urlparse, parse_qs, parse_qsl, urlencode


# 将中文转换为URL编码格式
def encode_to_url(url):
    return quote(url)


def decode_url(url_encoded):
    return unquote(url_encoded)


def url_query_dict(url: str):
    """
    解析url中的查询参数（?之后的内容）为字典
    """
    return parse_qs(urlparse(url).query)


def un_url_query_dict(params_dict: dict, if_quote=False):
    """
    url_query_dict函数的逆
    """
    return urlencode(params_dict, doseq=True) if if_quote else unquote(urlencode(params_dict, doseq=True))


def url_query_list(url: str):
    """
    解析url中的查询参数（?之后的内容）为列表
    """
    return parse_qsl(urlparse(url).query)


def un_url_query_list(params_list: list, if_quote=False):
    """
    url_query_list函数的逆
    """
    return urlencode(params_list) if if_quote else unquote(urlencode(params_list))
