# -*- encoding: utf-8 -*-
"""
@File Name      :   thread.py    
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

import threading
from queue import Queue


def create_threads(threads_num, target, args):
    """
    非可调用函数，只是示例函数
    """
    threads = []
    for i in range(threads_num):
        thread = threading.Thread(target=target, args=args, daemon=True)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def get_threads_results(threads_num, target, args):
    """
    能够获得线程的返回值的示例
    """
    threads = []
    threads_results = []
    que = Queue()
    for i in range(threads_num):
        thread = threading.Thread(target=lambda q, *arg: q.put(target(*arg)),
                                  args=args, daemon=True)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    while not que.empty():
        threads_results.extend(que.get())
    return threads_results
