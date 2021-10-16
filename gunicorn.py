import multiprocessing
import gevent
from gevent import monkey
from app.settings import basedir

monkey.patch_all()

# 绑定ip和端口号
bind = '0.0.0.0:8000'
# 监听队列
backlog = 512
# 进程数  cpu数量*2+1 推荐进程数
workers = multiprocessing.cpu_count() * 2 + 1
# 指定每个进程开启的线程数
threads = 3
# 处理请求的工作线程数，使用指定数量的线程运行每个worker。为正整数，默认为1。
worker_connections = 2000
# 进程守护True为开启后台模式，这里需要注意刚开始挂起最好使用False 看看脚本有没有反馈
daemon = True
# 设置超时时间120s，默认为30s。按自己的需求进行设置timeout = 120
timeout = 120
# 超时重启
graceful_timeout = 300
# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
# sync
# eventlet：需要下载eventlet>=0.9.7
# gevent：需要下载gevent>=0.13
# tornado：需要下载tornado>=0.2
# gthread
# gaiohttp：需要python 3.4和aiohttp>=0.21.5
worker_class = 'gevent'
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
# debug(调试)
# info(信息)
# warning(警告)
# error(错误)
# critical(危急)
loglevel = 'info'
# 设置gunicorn访问日志格式，错误日志无法设置
# 日志常见格式说明：
# 识别码	    说明
# h	        远程地址
# l	        “-“
# u	        用户名
# t	        时间
# r	        状态行，如：GET /test HTTP/1.1
# m	        请求方法
# U	        没有查询字符串的URL
# q	        查询字符串
# H	        协议
# s	        状态码
# B	        response长度
# b	        response长度(CLF格式)
# f	        参考
# a	        用户代理
# T	        请求时间，单位为s
# D	        请求时间，单位为ms
# p	        进程id
# {Header}i	请求头
# {Header}o	相应头
# {Variable}e	环境变量

access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 设置pid文件的文件名，如果不设置将不会创建pid文件
pidfile = "/logs/gunicorn.pid"
# 要写入的访问日志目录
accesslog = basedir + "/logs/gunicorn_access.log"
# 要写入错误日志的文件目录
errorlog = basedir + "/logs/gunicorn_error.log"
# 在keep-alive连接上等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间。
keepalive = 3
# HTTP请求行的最大大小，此参数用于限制HTTP请求行的允许大小，默认情况下，这个值为4094。
# 值是0~8190的数字。此参数可以防止任何DDOS攻击
limit_request_line = 5120

# 限制HTTP请求中请求头字段的数量。
# 此字段用于限制请求头字段的数量以防止DDOS攻击，与limit-request-field-size一起使用可以提高安全性。
# 默认情况下，这个值为100，这个值不能超过32768
limit_request_fields = 101

# 限制HTTP请求中请求头的大小，默认情况下这个值为8190。
# 值是一个整数或者0，当该值为0时，表示将对请求头大小不做限制
limit_request_field_size = 8190

# 设置gunicorn使用的python虚拟环境
# pythonpath = '/home/chenxinming/项目名//venv/bin/python3'

# 环境变量
raw_env = 'APE_API_ENV=DEV'
