# -*- encoding: utf-8 -*-
"""
@File Name      :   path.py    
@Create Time    :   2021/9/14 19:08
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

import os


def divide_dir_file(file_path):
    return os.path.dirname(file_path), os.path.basename(file_path)
