# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py
@Create Time    :   2021/7/12 15:40
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

import functools
import time
from concurrent import futures
from datetime import datetime
from threading import Timer

# 任务超时退出
executor = futures.ThreadPoolExecutor(1)


def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            future = executor.submit(func, *args, **kw)
            return future.result(timeout=seconds)
        return wrapper
    return decorator


# 类写法
# class timeout:
#     __executor = futures.ThreadPoolExecutor(1)
#
#     def __init__(self, seconds):
#         self.seconds = seconds
#
#     def __call__(self, func):
#         @functools.wraps(func)
#         def wrapper(*args, **kw):
#             future = timeout.__executor.submit(func, *args, **kw)
#             return future.result(timeout=self.seconds)
#         return wrapper


# 缓存
# 使用functools包下的LRU缓存即可

# 约束某个函数的可执行次数
class AllowCount:
    def __init__(self, count):
        self.count = count
        self.i = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if self.i >= self.count:
                return
            self.i += 1
            return func(*args, **kw)

        return wrapper


# 计算程序运行时间
def print_execute_time(function):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total running time: %s s" % (str(t1 - t0)))
        return result

    return wrapper

# 更精确的运行时间记录
def print_accurate_execute_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'函数 {func.__name__} 耗时 {(end - start) * 1000} ms')
        return res

    return wrapper

# 定时任务
class TimingTask(object):
    def __init__(self, start_time, interval, task_func, *args, **kwargs):
        """
        :params start:开始时间
        :params interval:间隔时间
        :params task_func:执行的函数
        :params args,kwargs:函数的参数
        """

        self.__timer = None
        self.__start_time = start_time
        self.__interval = interval
        self.__task_func = task_func
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

    def exec_callback(self):
        self.__task_func(*self.__args, **self.__kwargs)
        self.__timer = Timer(self.__interval, self.exec_callback)
        self.__timer.start()

    def start(self):
        interval = self.__interval - (datetime.now().timestamp() - self.__start_time.timestamp())
        self.__timer = Timer(interval, self.exec_callback)
        self.__timer.start()

    def cancel(self):
        self.__timer.cancel()
        self.__timer = None
