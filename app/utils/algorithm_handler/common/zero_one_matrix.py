# -*- encoding: utf-8 -*-
"""
@File Name      :   vector.py    
@Create Time    :   2021/8/3 22:06
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

import numpy as np
import pandas as pd

from app.utils.file_handler.text_handler.list import filter_empty_text
from app.utils.file_handler.text_handler.regex import replace_col_character


# 0-1矩阵
def rows_to_zero_one_matrix(rows):
    """
    :rows:[str,str...]
    """
    all_nodes_set = []
    table = []
    for row_text in rows:
        row_list = replace_col_character(row_text).split(',')
        table.append(row_list)
        all_nodes_set.extend(row_list)
    all_nodes_set = filter_empty_text(list(set(all_nodes_set)), method='space')
    return table_to_zero_one_matrix(table, all_nodes_set)


def table_to_zero_one_matrix(table, all_nodes_set):
    all_nodes_length = len(all_nodes_set)
    vector = [all_nodes_set]
    for row in table:
        vector_row = [0 for i in range(all_nodes_length)]
        for node in row:
            index = all_nodes_set.index(node)
            vector_row[index] = 1
        vector.append(vector_row)
    return vector


def zero_one_matrix_to_rows(zero_one_matrix):
    """
    vector:[[表头],[是否存在],[]...]
    """
    all_nodes_set = zero_one_matrix[0]
    zero_one_matrix_rows = zero_one_matrix[1:]
    text_list = []
    for row in zero_one_matrix_rows:
        vector_row = [all_nodes_set[index] for (index, value) in enumerate(row) if value == 1]
        text_list.append(','.join(vector_row))
    return text_list


def rows_to_zero_one_matrix_pd(rows):
    table = []
    for row_text in rows:
        row_list = re.sub(r'[，、]', ',', row_text).split(',')
        no_empty_row = list(set(filter_empty_text(row_list)))
        table.append(no_empty_row)
    all_nodes_set = list(set([node for row in table for node in row]))
    return table_to_zero_one_matrix_pd(table, all_nodes_set)


def table_to_zero_one_matrix_pd(table, all_nodes_set):
    zero_one_matrix = pd.DataFrame(np.zeros([len(table), len(all_nodes_set)]), columns=all_nodes_set)
    for i in range(len(table)):
        columns = [ele for ele in table[i]]
        zero_one_matrix.loc[i, columns] = 1
    return zero_one_matrix


def zero_one_matrix_to_rows_pd(zero_one_matrix):
    all_nodes_set = zero_one_matrix.columns.values
    # print(all_nodes_set)
    zero_one_matrix_rows = zero_one_matrix.to_numpy()
    # print(zero_one_matrix_rows)
    # 更快的写法
    text_list = [','.join([all_nodes_set[index] for (index, value) in enumerate(row) if value == 1]) for row in
                 zero_one_matrix_rows]
    # 一般写法
    # text_list=[]
    # for row in zero_one_matrix_rows:
    #     vector_row=[all_nodes_set[index] for (index,value) in enumerate(row) if value ==1]
    #     text_list.append(','.join(vector_row))
    return text_list

# print(zero_one_matrix_to_rows(rows_to_zero_one_matrix(['1,2,3','2,4,5','5,6,7','3,4,7','6,5,1'])))
# print(zero_one_matrix_to_rows_pd(rows_to_zero_one_matrix_pd(['1,2,3','2,4,5','5,6,7','3,4,7','6,5,1'])))
