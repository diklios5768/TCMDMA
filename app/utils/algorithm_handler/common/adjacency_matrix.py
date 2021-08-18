# -*- encoding: utf-8 -*-
"""
@File Name      :   adjacency_matrix.py    
@Create Time    :   2021/8/3 21:44
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
import networkx as nx
from app.utils.algorithm_handler.common.zero_one_matrix import rows_to_zero_one_matrix_pd


# 相关性(非概率)邻接矩阵算法
def correlation_adjacency_matrix(a, b):
    relation = np.sum(np.logical_and(a, b)) / len(a)
    if 0 < relation <= 1:
        return 1
    else:
        return 0


# 带次数的相关性邻接矩阵算法
def correlation_adjacency_matrix_with_frequency(a, b):
    return np.sum(np.logical_and(a, b))


# 0-1矩阵到邻接矩阵
def zero_one_matrix_to_adjacency_matrix_pd(zero_one_matrix):
    adjacency_matrix = zero_one_matrix.corr(method=correlation_adjacency_matrix)
    adjacency_matrix.values[tuple([np.arange(adjacency_matrix.shape[0])]) * 2] = 0
    return adjacency_matrix


def zero_one_matrix_to_adjacency_matrix_with_frequency_pd(zero_one_matrix):
    adjacency_matrix = zero_one_matrix.corr(method=correlation_adjacency_matrix_with_frequency)
    adjacency_matrix.values[tuple([np.arange(adjacency_matrix.shape[0])]) * 2] = 0
    return adjacency_matrix


# 两两之间条件概率算法
def contingent_probability(a, b):
    return np.sum(np.logical_and(a, b)) / np.sum(a)


# 0-1矩阵到条件概率
def zero_one_matrix_to_contingent_probability(zero_one_matrix):
    confidence = zero_one_matrix.corr(method=contingent_probability)
    return confidence
