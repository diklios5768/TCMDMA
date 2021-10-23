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
from app.libs.lists import not_pagination


def params_status(database_class,status=1):
    return [database_class.status==status]


def params_remove_pagination(params_dict: dict):
    if params_dict is None:
        return NoDataError()
    for key in list(params_dict.keys()):
        if key in not_pagination:
            params_dict.pop(key)
    return params_dict


def params_remove_empty(params_dict: dict):
    for key in list(params_dict.keys()):
        if not params_dict[key]:
            params_dict.pop(key)
    return params_dict


def params_fuzzy_query(database_class, params_dict):
    return [database_class.__dict__[key].like('%{}%'.format(value)) for key, value in params_dict.items()]


def params_antd_table_return(rows):
    class_rows = []
    for row in rows:
        row.create_time *= 1000
        dataset_row = dict(row)
        dataset_row['key'] = dataset_row['id']
        class_rows.append(dataset_row)
    class_rows.reverse()
    return class_rows
