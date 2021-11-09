# -*- encoding: utf-8 -*-
"""
@File Name      :   commands.py    
@Create Time    :   2021/11/2 8:43
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

import os
import click

from app.models.create_db import init_db, drop_db, recreate_db
from app.models.tcm.development import init_development_data, update_development_data
from app.models.tcm.production import init_production_data, update_production_data
from app.viewModels.common import init_redis_production, init_redis_development
from app.utils.file_handler import copy_dir, move_dir


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
            init_redis_production()
            click.echo('production data init success')
        elif env in ['development', 'dev', 'd']:
            init_development_data()
            init_redis_development()
            click.echo('development data init success')
        else:
            click.echo('no this env')

    # 开发数据
    @app.cli.command()
    @click.option('--env', prompt='input environment', help='Choose environment.')
    def data_update(env):
        if env in ['production', 'prod', 'p']:
            update_production_data()
            init_redis_production()
            click.echo('production data update success')
        elif env in ['development', 'dev', 'd']:
            update_development_data()
            init_redis_development()
            click.echo('development data update success')

    @app.cli.command()
    @click.option('--dir_path', prompt='input absolute folder to copy users data', help='Copy users data.')
    def copy_user_data(dir_path):
        if os.path.isdir(dir_path):
            copy_dir(app.config['USER_DIR'], dir_path)
            click.echo('move success')
        else:
            click.echo('invalid dir path')

    # 快速备份用户数据
    @app.cli.command()
    @click.option('--dir_path', prompt='input absolute folder to move users data', help='Move users data.')
    def move_user_data(dir_path):
        if os.path.isdir(dir_path):
            move_dir(app.config['USER_DIR'], dir_path)
            click.echo('move success')
        else:
            click.echo('invalid dir path')
