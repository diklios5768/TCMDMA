# -*- encoding: utf-8 -*-
"""
@File Name      :   tree.py    
@Create Time    :   2021/7/24 15:13
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


# 递归处理树结构
def handle_tree(tree):
    for child in tree:
        node_id = child.get('id')
        node_title = child.get('title')
        node_class = child.get('class')
        node_children = child.get('children', None)
        if node_children is not None:
            handle_tree(node_children)
