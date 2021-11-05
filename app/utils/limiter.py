# -*- encoding: utf-8 -*-
"""
@File Name      :   limiter.py    
@Create Time    :   2021/11/2 22:33
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

from flask import request

from app.register.extensions import limiter

# 不限制
exempt_limiter = limiter.exempt
# 单独限制
test_limiter = limiter.limit('1/second;5/minute')
# 注册限制
register_limit = limiter.limit('1/second;2/minute;5/hour;10/day')

# 共享限制
# 数据库访问限制
mysql_limit = limiter.shared_limit("100/hour", scope="mysql")


# 服务端访问限制
def host_scope(endpoint_name):
    return request.host


host_limit = limiter.shared_limit("100/hour", scope=host_scope)


# @limiter.request_filter这个装饰器只是将一个函数标记为将要测试速率限制的请求的过滤器
# 如果任何请求过滤器返回True，则不会对该请求执行速率限制。此机制可用于创建自定义白名单
# @limiter.request_filter
# def ip_whitelist():
#     return request.remote_addr == "127.0.0.1"
#
#
# @limiter.request_filter
# def header_whitelist():
#     return request.headers.get("X-Internal", "") == "true"
