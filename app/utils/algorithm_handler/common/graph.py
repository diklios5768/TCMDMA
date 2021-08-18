# -*- encoding: utf-8 -*-
"""
@File Name      :   graph.py    
@Create Time    :   2021/8/4 14:27
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

import networkx as nx


def adjacency_matrix_to_networkx_graph_pd(adjacency_matrix):
    return nx.from_pandas_adjacency(adjacency_matrix)
