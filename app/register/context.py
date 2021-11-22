# -*- encoding: utf-8 -*-
"""
@File Name      :   context.py    
@Create Time    :   2021/11/2 8:42
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

from flask import request, make_response

from app.libs.error_exception import IPAddressBanned
from app.viewModels.common.ip import is_banned_ip_address


# 注册上下文
def register_context(app):
    register_request_context(app)
    # register_shell_context(app)
    # register_template_context(app)
    # register_jinja2(app)


# 注册全局的请求处理
def register_request_context(app):
    # # 钩子函数 before_first_request
    # @app.before_first_request
    # def before_first():
    #     print("app.before_first")

    # 钩子函数 before_request
    @app.before_request
    def limit_remote_address():
        remote = request.remote_addr
        if is_banned_ip_address(remote):
            raise IPAddressBanned()

    # # 钩子函数 after_request
    # @app.after_request
    # def make_cors(resp):
    #     """
    #     #请求钩子，在所有的请求发生后执行，加入headers，用于跨域。
    #     :param resp:
    #     :return:
    #     """
    #     resp = make_response(resp)
    #     resp.headers['Access-Control-Allow-Origin'] = '*'
    #     resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    #     resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    #     return resp
    #
    # # 钩子函数 teardown_request
    # @app.teardown_request
    # def teardown(e):
    #     print("app.teardown" + str(e))


# 注册shell上下文
def register_shell_context(app):
    # 配置shell的上下文
    @app.shell_context_processor
    def make_shell_context():
        return dict()


# 注册模板上下文
def register_template_context(app):
    # 下面的都是例子，实际上没有用
    pass

    # 注册模板上下文处理函数
    # 可以代替在所有路由重复传入一个值，然后在模板中使用
    # 在render_template之前执行，函数返回值会被添加到模板中，即完成了注册模板全局变量
    @app.context_processor
    def inject_foo():
        return dict(foo='foo')

    # 注册自定义模板全局函数，可以在模板中调用函数
    @app.template_global
    def bar():
        return 'bar'

    # 注册自定义模板过滤器
    @app.template_filter
    def musical(s):
        return s + ''

    # 注册自定义的模板测试器
    @app.template_test()
    def bza(n):
        if n == 'bza':
            return True
        else:
            return False


# 更改jinja2设置
def register_jinja2(app):
    # 下面的都是例子，实际上没有用
    pass
    # 添加自定义全局变量
    foo = 'a'
    app.jinja_env.globals['foo'] = foo

    # 添加自定义全局函数
    def bar():
        return 'b'

    app.jinja_env.globals['bar'] = bar

    # 添加自定义过滤器
    def smile(s):
        return s + 'c'

    app.jinja_env.filters['smile'] = smile

    # 添加自定义全局测试器
    def bza(n):
        if n == 'bza':
            return True
        else:
            return False

    app.jinja_env.tests['bza'] = bza

    # 修改界定符
    # app.jinja_env.block_start_string = '(%'  # 修改块开始符号
    # app.jinja_env.block_end_string = '%)'  # 修改块结束符号
    # app.jinja_env.variable_start_string = '(('  # 修改变量开始符号
    # app.jinja_env.variable_end_string = '))'  # 修改变量结束符号
    # app.jinja_env.comment_start_string = '(#'  # 修改注释开始符号
    # app.jinja_env.comment_end_string = '#)'  # 修改注释结束符号
