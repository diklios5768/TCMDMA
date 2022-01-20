# -*- encoding: utf-8 -*-
"""
@File Name      :   read.py    
@Create Time    :   2022/1/14 15:27
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

from itertools import islice
from typing import List, Iterable


def count_file_lines(file_path: str, per: int = 1000) -> int:
    """
    计算文件行数
    """
    with open(file_path, 'r') as f:
        stop = False
        count = 0
        while not stop:
            lines = list(islice(f, per))
            if lines:
                count += len(list(lines))
                print(f'读取了{count}行')
            else:
                stop = True
        return count


def read_n_lines_each_time(file_path: str, per: int = 1000) -> Iterable[List[str]]:
    """
    每次读取文件n行，返回迭代器
    """
    with open(file_path, 'r') as f:
        stop = False
        while not stop:
            lines = list(islice(f, per))
            if lines:
                yield lines
            else:
                stop = True
