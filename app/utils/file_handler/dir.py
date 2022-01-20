# -*- encoding: utf-8 -*-
"""
@File Name      :   dir.py    
@Create Time    :   2022/1/14 15:26
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

import os


def read_dir_files_name(file_dir):
    """
    只处理一层文件夹
    """
    file_names = []
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        names = os.listdir(file_dir)
        for name in names:
            if os.path.isfile(os.path.join(file_dir, name)):
                file_names.append(name)
    return file_names
