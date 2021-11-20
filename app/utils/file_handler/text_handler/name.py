# -*- encoding: utf-8 -*-
"""
@File Name      :   name.py    
@Create Time    :   2021/11/20 19:28
@Description    :   主流命名法之间的转换
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
@other information
"""
__auth__ = 'diklios'

import re


def pascal_case_to_snake_case(pascal_case: str) -> str:
    """大驼峰（帕斯卡）转蛇形"""
    snake_case = re.sub(r"(?P<key>[A-Z])", r"_\g<key>", pascal_case)
    return snake_case.lower().strip('_')


def pascal_case_dict_to_snake_case_dict(pascal_case_dict: dict = None) -> dict:
    """
    大驼峰（帕斯卡）字典转下划线字典
    :params pascal_case_dict:大驼峰命名的字典
    """
    if pascal_case_dict is None:
        return {}
    return {pascal_case_to_snake_case(key): value for key, value in pascal_case_dict.items()}


def snake_case_to_pascal_case(snake_case: str) -> str:
    """蛇形转大驼峰（帕斯卡）"""
    words = snake_case.split('_')
    return ''.join(word.title() for word in words)


def snake_case_dict_to_pascal_case_dict(snake_case_dict: dict = None) -> dict:
    """
    下划线字典转大驼峰字典
    :params snake_case_dict:下划线命名的字典
    """
    if snake_case_dict is None:
        return {}
    return {snake_case_to_pascal_case(key): value for key, value in snake_case_dict.items()}


def snake_case_to_camel_case(snake_case: str) -> str:
    """下划线转小驼峰"""
    return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), snake_case)


def snake_dict_to_camel_dict(snake_dict: dict = None) -> dict:
    """
    下划线字典转小驼峰字典
    :params snake_dict:下划线命名的字典
    """
    if snake_dict is None:
        return {}
    return {snake_case_to_camel_case(key): value for key, value in snake_dict.items()}


def camel_case_to_snake_case(camel_case: str) -> str:
    """小驼峰转下划线"""
    if '_' not in camel_case:
        camel = re.sub(r'([a-z])([A-Z])', r'\1_\2', camel_case)
    else:
        raise ValueError('{camel}字符中包含下划线，无法转换')
    return camel.lower()


def camel_dict_to_snake_case_dict(camel_dict: dict = None) -> dict:
    """
    小驼峰字典转下划线字典
    :params camel_dict:小驼峰命名的字典
    """
    if camel_dict is None:
        return {}
    return {camel_case_to_snake_case(key): value for key, value in camel_dict.items()}


def pascal_case_to_camel_case(pascal_case: str) -> str:
    """大驼峰转小驼峰"""
    return snake_case_to_camel_case(pascal_case_to_snake_case(pascal_case))


def pascal_case_dict_to_camel_case_dict(pascal_case_dict: dict = None) -> dict:
    """
    大驼峰字典转小驼峰字典
    :params pascal_case_dict:大驼峰命名的字典
    """
    if pascal_case_dict is None:
        return {}
    return {pascal_case_to_camel_case(key): value for key, value in pascal_case_dict.items()}


def camel_case_to_pascal_case(camel_case: str) -> str:
    """小驼峰转大驼峰"""
    return snake_case_to_pascal_case(camel_case_to_snake_case(camel_case))


def camel_case_dict_to_pascal_case_dict(camel_case_dict: dict = None) -> dict:
    """
    小驼峰字典转大驼峰字典
    :params camel_case_dict:小驼峰命名的字典
    """
    if camel_case_dict is None:
        return {}
    return {camel_case_to_pascal_case(key): value for key, value in camel_case_dict.items()}
