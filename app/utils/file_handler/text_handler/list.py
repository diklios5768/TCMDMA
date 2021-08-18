# -*- encoding: utf-8 -*-
"""
@File Name      :   list.py    
@Create Time    :   2021/7/24 15:15
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


# 列表递归
def handle_deep_texts_list(lists):
    child = lists[0]
    if isinstance(child, list):
        for each_list in lists:
            handle_deep_texts_list(each_list)
    else:
        for (index, val) in enumerate(lists):
            # do something
            # attention:将想做的操作替换下面的代码
            lists[index] = val


# 列表转置
# 最基础的 for 循环
def transpose_for(data):
    transposed = []
    for i in range(len(data[0])):
        new_row = []
        for row in data:
            new_row.append(row[i])
        transposed.append(new_row)
    return transposed


# 使用列表推导式 List Comprehension
def transpose_list_comprehension(data):
    transposed = [[row[i] for row in data] for i in range(len(data[0]))]
    return transposed


# 使用 zip(*iterable) 函数（推荐）
def transpose_zip(data):
    # transposed = list(zip(*data))
    # [(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]
    # 注意 zip 本身返回的数据类型为 tuple 元组
    # 其中符号 * 号可以对元素进行解压或展开

    transposed = list(map(list, zip(*data)))
    return transposed

# 还有numpy和pandas的：https://www.cnblogs.com/MoonYear530/p/13697120.html
