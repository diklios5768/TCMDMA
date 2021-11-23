# -*- encoding: utf-8 -*-
"""
@File Name      :   table.py    
@Create Time    :   2021/11/1 19:30
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


# 列表递归
def handle_deep_texts_list(lists):
    child = lists[0]
    if isinstance(child, list):
        for each_list in lists:
            handle_deep_texts_list(each_list)
    else:
        for (index, val) in enumerate(lists):
            lists[index] = replace_character(val)


# 文本分行
def texts_to_rows(text, method='character', character=';'):
    rows = []
    if method == "enter":
        rows = text.splitlines()
    elif method == "character":
        rows = text.split(character)
    rows = filter_empty_text(rows, method='empty')
    return rows


# 行数据转二维数组
def rows_to_table_data(rows: list, character=','):
    table_data = []
    for row in rows:
        row_data = row.split(character)
        table_data.append(filter_empty_text(row_data, method='empty'))
    return table_data


# 一维数组转二维的单列数组
def rows_to_single_col_table_data(rows: list):
    return [[row] for row in rows]


# 完整文本数据转化为行数据预处理流程
def texts_to_rows_integral_process(text):
    return texts_to_rows(replace_character(text))


def texts_to_table_data_integral_process(text):
    return rows_to_table_data(texts_to_rows(replace_character(text)))


def texts_to_single_col_table_data_integral_process(text):
    return rows_to_single_col_table_data(texts_to_rows(replace_character(text)))
