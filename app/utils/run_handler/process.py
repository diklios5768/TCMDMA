# -*- encoding: utf-8 -*-
"""
@File Name      :   process.py    
@Create Time    :   2022/1/14 15:30
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

import multiprocessing


def create_processes(processes_num, target, args):
    """
    非可调用函数，只是示例函数
    """
    processes = []
    for i in range(processes_num):
        process = multiprocessing.Process(target=target, args=args,daemon=True)
        processes.append(process)
    for process in processes:
        process.start()
    for process in processes:
        process.join()
