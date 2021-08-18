# -*- encoding: utf-8 -*-
"""
@File Name      :   params.py    
@Create Time    :   2021/7/30 11:48
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

from app.libs.error_exception import NoDataError


def params_ready(params_dict: dict):
    if params_dict is None:
        return NoDataError()
    remove_list = ["current", "pageSize"]
    for key in list(params_dict.keys()):
        if key in remove_list:
            params_dict.pop(key)
    filters_by = params_dict
    return filters_by
