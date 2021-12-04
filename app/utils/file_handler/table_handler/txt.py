# -*- encoding: utf-8 -*-
"""
@File Name      :   txt.py
@Create Time    :   2021/11/18 16:48
@Description    :
@Version        :
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
@other information
"""
__auth__ = 'diklios'

import pandas as pd

from app.utils.file_handler.text_handler.regex import replace_row_character
from app.utils.file_handler.text_handler.table import texts_to_table_data_integral_process


def read_txt_table_large_file(file_path: str, sep: str = '\t',
                              row_start: int = None, row_end: int = None,
                              col_start: int = None, col_end: int = None, ) -> list[list[str, ...]]:
    """
    默认换行是回车
    必须确保是正确的表格形式的文本，而不是单列文本，否则会导致列选择错误
    读取大文件不允许行的切片从后向前读取，因为会导致内存溢出，所以row_start,row_end>=0,row_end>=row_start
    :params file_path:文件路径
    :return 二维列表
    """
    if not row_start:
        row_start = 0
    if not row_end:
        row_end = 0
    if row_end <= row_start or row_start < 0 or row_end < 0:
        return []
    done = 0
    row_count = -1
    table_data = []
    with open(file_path, 'r') as f:
        while not done:
            line = f.readline()
            row_count += 1
            if row_count < row_start:
                continue
            if row_count >= row_end:
                done = 1
            if line == '':
                done = 1
            else:
                row = replace_row_character(line).replace(';', '').split(sep)[col_start:col_end]
                table_data.append(row)
    return table_data


def read_txt_table_one_time(file_path: str,
                            row_start: int = None, row_end: int = None,
                            col_start: int = None, col_end: int = None) -> list[list[str, ...]]:
    """
    默认换行是回车
    必须确保是正确的表格形式的文本，而不是单列文本，否则会导致列选择错误
    :params file_path:文件路径
    :return 二维列表
    """
    with open(file_path, 'r') as f:
        return texts_to_table_data_integral_process(f.read())[row_start:row_end, col_start:col_end]


def generate_txt_table(file_path: str, table_data: list[list[str, ...]]) -> bool:
    try:
        if table_data and file_path:
            with open(file_path, 'w') as f:
                f.write('\n'.join(['\t'.join(row) for row in table_data]))
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False


def read_txt_table_by_pandas(filepath_or_buffer, sep: str = '\t') -> tuple[list[list[str, ...]], pd.DataFrame]:
    """
    :params filepath_or_buffer:文件路径或者URL
    :params sep:指定分隔符
    """
    df = pd.read_table(filepath_or_buffer, sep=sep)
    return df.to_numpy().tolist(), df
