import os
import click
from flask import request, make_response, g
from werkzeug.exceptions import HTTPException

from .my_flask import Flask
from .extensions import cors
from .settings import config
from .logging import file_log_handler
# 数据库相关处理
from .models import db, migrate
from .models.tcm.production import init_production_data,update_production_data
from .models.create_db import init_db, drop_db, recreate_db
from .views import tcm_bp
from .utils.mail_handler import mail
from .libs.error import APIException
from .libs.error_exception import ServerError


# 工厂函数


def create_app(config_name=None):
    if config_name is None:
        # 获取环境设置
        config_name = os.getenv('FLASK_ENV', 'development')
    # 创建APP
    app = Flask(__name__)
    register_config(app, config_name)
    register_extensions(app)
    register_blueprints(app)
    # 日志注册尽量在前面
    register_logging(app)
    register_commands(app)
    # register_context(app)
    register_errors(app)

    return app


# 加载各种配置
def register_config(app, config_name):
    # 根据环境加载配置
    # 也可以使用app.config.from_json()加载json数据
    app.config.from_object(config[config_name])


# 注册插件,全部使用init_app的方法生成
def register_extensions(app):
    # 切记数据库生成的代码必须放在数据库相关配置都配置好了之后再生成,这点非常重要
    db.init_app(app)
    # 数据库迁移
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app, supports_credentials=True)


# 注册路由
def register_blueprints(app):
    app.register_blueprint(tcm_bp, url_prefix='/')


# 注册命令
def register_commands(app):
    # 配置一些flask的命令，终端输入 flask 函数名，即可调用
    # 通过命令行快速构建数据库
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Drop databases.')
    @click.option('--recreate', is_flag=True,
                  help='Create databases after drop.')
    @click.option('--bind', default=None, help='appoint which database to operate.')
    def db_init(drop, recreate, bind):
        if drop:
            click.confirm(
                'This option will delete the database,do you want to continue?',
                abort=True)
            drop_db(bind)
            click.echo('Dropped database')
        elif recreate:
            click.confirm(
                'This option will delete the database and create new database,do you want to continue?',
                abort=True)
            recreate_db(bind)
            click.echo('Recreated database')
        else:
            init_db(bind)
            click.echo('Initialized database')

    # 生成生产数据
    # 生成数据
    @app.cli.command()
    @click.option('--env', prompt='input environment', help='Choose environment to run init data function.')
    def data_init(env):
        if env in ['production', 'prod', 'p']:
            init_production_data()
        click.echo('data init success')

    @app.cli.command()
    @click.option('--env', prompt='input environment', help='Choose environment.')
    def data_update(env):
        if env in ['production', 'prod', 'p']:
            update_production_data()
        click.echo('data update success')


# 注册上下文
def register_context(app):
    register_request_context(app)
    register_shell_context(app)
    register_template_context(app)
    register_jinja2(app)


# 注册全局的请求处理
def register_request_context(app):
    # 钩子函数 before_first_request
    @app.before_first_request
    def before_first():
        print("app.before_first")

    # 钩子函数 before_request
    @app.before_request
    def before():
        data = request.get_json()
        if data is None:
            data = request.args.to_dict()
        g.data = data
        print("app.before")

    # 钩子函数 after_request
    @app.after_request
    def make_cors(resp):
        """
        #请求钩子，在所有的请求发生后执行，加入headers，用于跨域。
        :param resp:
        :return:
        """
        resp = make_response(resp)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return resp

    # 钩子函数 teardown_request
    @app.teardown_request
    def teardown(e):
        print("app.teardown" + str(e))


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


# 注册错误处理函数
def register_errors(app):
    # 1.0以后才能捕捉到所有的异常，返回格式改为通用的格式
    # 注意这里只捕捉了异常，成功的并不会被捕捉
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 999
            return APIException(success=False, code=code, error_code=error_code, msg=msg)
        else:
            # 调试模式的时候显示错误信息
            if not app.config['DEBUG']:
                return ServerError()
            else:
                raise e


# 日志系统配置
def register_logging(app):

    app.logger.addHandler(file_log_handler)
