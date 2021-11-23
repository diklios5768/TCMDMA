# -*- encoding: utf-8 -*-
"""
@File Name      :   heterogeneous.py    
@Create Time    :   2021/11/2 23:15
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

from app.utils.file_handler.text_handler.list import filter_empty_text
from app.utils.file_handler.text_handler.regex import replace_character


def heterogeneous_relational_analysis(table_data, combination: float):
    table_list = []
    table_items = []
    for row in table_data:
        row_list = []
        row_items = []
        for col in row:
            col_list = filter_empty_text(replace_character(col).split(','))
            row_list.append(col_list)
            row_items.extend(col_list)
        table_list.append(row_list)
        table_items.extend(row_items)
