import os

from app.register import Flask
from app.register.blueprints import register_blueprints
from app.register.commands import register_commands
from app.register.errors import register_errors
from app.register.extensions import register_extensions
from app.register.logger import register_logger
from app.register.context import register_context
from .settings import config


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
    register_logger(app)
    register_commands(app)
    register_context(app)
    register_errors(app)

    return app


# 加载各种配置
def register_config(app, config_name):
    # 根据环境加载配置
    # 也可以使用app.config.from_json()加载json数据
    app.config.from_object(config[config_name])
