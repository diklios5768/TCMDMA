# -*- encoding: utf-8 -*-
"""
@File Name      :   pandas.py    
@Create Time    :   2021/11/18 17:09
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

from typing import Union

import pandas as pd


def table_data_to_dataframe(table_data: list[list[str, ...]] = None) -> Union[pd.DataFrame, bool]:
    """
    将列表转换为dataframe
    :param table_data:
    :return:
    """
    if table_data:
        return pd.DataFrame(table_data)
    else:
        return False


def dataframe_to_table_data(dataframe: pd.DataFrame = None):
    if dataframe:
        return dataframe.to_numpy().tolist()
    else:
        return False
