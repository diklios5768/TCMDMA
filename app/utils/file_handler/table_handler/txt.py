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


def read_txt_table_by_pandas(filepath_or_buffer, sep: str = '\t'):
    """
    :params filepath_or_buffer:文件路径或者URL
    :params sep:指定分隔符
    """
    df = pd.read_table(filepath_or_buffer, sep=sep)
    return df.to_numpy().tolist(), df
