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

import numpy as np

from app.utils.algorithm_handler.common.zero_one_matrix import table_to_zero_one_matrix
from app.utils.file_handler.text_handler.list import filter_empty_text
from app.utils.file_handler.text_handler.regex import replace_character


def heterogeneous_relational_analysis(table_data, min_co_occurrence_frequency: int, combination: float):
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
    table_list_len = len(table_list)
    networks = [heterogeneous_associated_network(table_list[i], table_list[j], min_co_occurrence_frequency)
                for i in range(table_list_len) for j in range(i+1, table_list_len)]
    # todo:组合（多种组合）并计算联合度，最后排序
    # todo:封装算法生成分析结果文件


def heterogeneous_associated_network(z_table, w_table, min_co_occurrence_frequency: int):
    """
    :params min_co_occurrence_frequency:最小共现次数，超过的才认为是有效的规则
    """
    z_table_zero_one_matrix = table_to_zero_one_matrix(z_table)
    z_nodes = z_table_zero_one_matrix[0]
    z_matrix = np.array(z_table_zero_one_matrix[1:]).T
    z_matrix_length = len(z_matrix)
    z_matrix_frequency = [np.sum(vector) for vector in z_matrix]
    w_table_zero_one_matrix = np.array(table_to_zero_one_matrix(w_table))
    w_nodes = w_table_zero_one_matrix[0]
    w_matrix = np.array(w_table_zero_one_matrix[1:]).T
    w_matrix_length = len(w_matrix)
    w_matrix_frequency = [np.sum(vector) for vector in w_matrix]
    co_occurrence_matrix = np.zeros((z_matrix_length, w_matrix_length))
    rules = {}
    for i in range(z_matrix_length):
        for j in range(w_matrix_length):
            co_occurrence_frequency = np.sum(np.logical_and(z_matrix[i], w_matrix[j]))
            co_occurrence_matrix[i, j] = co_occurrence_frequency
            if co_occurrence_frequency >= min_co_occurrence_frequency:
                rules[(z_nodes[i], w_nodes[j])] = co_occurrence_frequency
    return {
        'rules': rules, 'co_occurrence_matrix': co_occurrence_matrix,
        'z_nodes': z_nodes, 'z_matrix_frequency': z_matrix_frequency,
        'z_nodes_frequency': dict(zip(z_nodes, z_matrix_frequency)),
        'w_nodes': w_nodes, 'w_matrix_frequency': w_matrix_frequency,
        'w_nodes_frequency': dict(zip(w_nodes, w_matrix_frequency)),
    }
