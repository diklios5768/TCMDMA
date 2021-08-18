# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/8/3 21:43
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

from app.utils.algorithm_handler.common.zero_one_matrix import rows_to_zero_one_matrix_pd
from app.utils.algorithm_handler.common.adjacency_matrix import zero_one_matrix_to_adjacency_matrix_pd, \
    zero_one_matrix_to_adjacency_matrix_with_frequency_pd
from app.utils.algorithm_handler.common.graph import adjacency_matrix_to_networkx_graph_pd


def rows_to_graph(rows):
    return adjacency_matrix_to_networkx_graph_pd(
        zero_one_matrix_to_adjacency_matrix_pd(rows_to_zero_one_matrix_pd(rows)))


def rows_to_graph_with_weight(rows):
    return adjacency_matrix_to_networkx_graph_pd(
        zero_one_matrix_to_adjacency_matrix_with_frequency_pd(rows_to_zero_one_matrix_pd(rows)))
