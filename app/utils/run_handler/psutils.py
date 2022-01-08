# -*- encoding: utf-8 -*-
"""
@File Name      :   psutils.py    
@Create Time    :   2022/1/8 10:45
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

import psutil


def get_system_cpu_info():
    """
    系统的CPU利用情况
    :user:用户的cpu时
    """
    return psutil.cpu_times()


def get_system_cpu_count(logical=True):
    """
    获取cpu逻辑和物理个数
    logical值为True时，返回逻辑cpu个数，为False时，返回物理cpu个数
    """
    return psutil.cpu_count(logical=logical)


def get_system_cpu_percent(interval):
    """
    获取系统cpu利用率
    :interval:间隔时间，为0.0或者None的时候，需要调用两次
    """
    return psutil.cpu_percent(interval=interval)


def get_system_memory_info():
    """
    系统的内存利用情况
    """
    return psutil.virtual_memory()


def get_system_disk_partitions_info():
    """
    获得磁盘分区信息
    """
    return psutil.disk_partitions()


def get_system_partition_info(partition='/'):
    """
    获得某个分区的信息
    """
    return psutil.disk_usage(partition)


def get_system_io_info(per_disk=True):
    """
    获取硬盘总的io数和读写信息或者每一个分区的信息
    """
    return psutil.disk_io_counters(perdisk=per_disk)


def get_system_net_info(per_nic=True):
    """
    获取网络总的信息或者每一个网卡的信息
    """
    return psutil.net_io_counters(pernic=per_nic)


def get_process(process_name: str) -> list:
    """
    p.name():进程名
    p.exe():进程的bin路径
    p.cwd():进程的工作目录绝对路径
    p.status():进程状态
    p.create_time():进程创建时间
    p.uids():进程uid信息
    p.gids():进程的gid信息
    p.cpu_times():进程的cpu时间信息,包括user,system两个cpu信息
    p.cpu_affinity():get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
    p.memory_percent():进程内存利用率
    p.memory_info():进程内存rss,vms信息
    p.io_counters():进程的IO信息,包括读写IO数字及参数
    p.connectios():返回进程列表
    p.num_threads():进程开启的线程数
    """
    processes = []
    # 获取当前系统所有进程id列表
    all_pids = psutil.pids()

    # 遍历所有进程，名称匹配的加入process_list
    for pid in all_pids:
        p = psutil.Process(pid)
        if p.name() == process_name:
            processes.append(p)
    return processes


def get_processes_memory_info(processes: list[psutil.Process]) -> list:
    return [{
        'name': process.name(),
        'pid': process.pid,
        'memory': process.memory_info().rss,
        'memory_percent': process.memory_percent(),
    } for process in processes]


def get_processes_cpu_info(processes: list[psutil.Process]):
    """
    第一次调用process_instance.cpu_percent(None)得到的是0
    第二次调用process_instance.cpu_percent(None)得到的是从上一次调用同一个进程对象的cpu_percent(None)方法到第二次调用之间的cpu利用率
    cpu利用率是计算一段时间内cpu计算时间 / 总时间
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for process in processes:
                process.cpu_percent(None)
            result = func(*args, **kwargs)
            info = [{
                'name': process.name(),
                'pid': process.pid,
                'cpu_percent': process.cpu_percent(None)
            } for process in processes]
            print(info)
            return result

        return wrapper

    return decorator


print(get_system_net_info(False))
