# -*- encoding: utf-8 -*-
"""
@File Name      :   set.py    
@Create Time    :   2022/1/12 11:02
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'


# 交集
def intersection_set(list1, list2):
    return list(set(list1) & set(list2))


# 并集
def union_set(list1, list2):
    return list(set(list1) | set(list2))


# 差集或者补集
def difference_set(list1, list2):
    return list(set(list1) - set(list2))


# 对称差集
# 项在list1或list2中，但不会同时出现在二者中
def symmetric_difference_set(list1, list2):
    return list(set(list1) ^ set(list2))
