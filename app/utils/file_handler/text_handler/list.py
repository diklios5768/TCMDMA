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

from app.utils.file_handler.text_handler.string import filter_space


# 分组
def group(list_to_group, step: int = 10):
    return [list_to_group[i:i + step] for i in range(0, len(list_to_group), step)]


# 过滤列表中的空字符
def filter_empty_text(li, method='empty'):
    # 只过滤空字符、None、[]
    if method == 'empty':
        return list(filter(None, li))
    # 过滤只含有空格的字符，如果字符中不仅含有空格，还有其他能显示的字符则不过滤，如' space  '
    elif method == "space":
        return list(filter(filter_space, li))
    elif method == 'all':
        filtered_none_list = filter(None, li)
        filtered_space_list = list(filter(filter_space, filtered_none_list))
        return filtered_space_list


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

# 交集
def intersection(list1,list2):
    return list(set(list1)&set(list2))

# 并集
def union_set(list1,list2):
    return list(set(list1)|set(list2))

# 差集或者补集
def difference_set(list1,list2):
    return list(set(list1)-set(list2))

# 对称差集
# 项在list1或list2中，但不会同时出现在二者中
def symmetric_difference_set(list1,list2):
    return list(set(list1)^set(list2))
