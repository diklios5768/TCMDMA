# -*- encoding: utf-8 -*-
"""
@File Name      :   blueprints.py    
@Create Time    :   2021/11/2 8:52
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

from app.views import main_bp


# 注册路由
def register_blueprints(app):
    app.register_blueprint(main_bp, url_prefix='/')
