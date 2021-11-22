# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/11/22 10:02
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
@other information
"""
__auth__ = 'diklios'
from flask import Blueprint, render_template, current_app, jsonify, url_for

from app.views.tcm.api import api_bp

# 第一个参数是蓝图的名称，第二个参数是蓝图位置信息
tcm_bp = Blueprint('tcm', __name__)
tcm_bp.register_blueprint(api_bp, url_prefix='/api')


@tcm_bp.get('/', defaults={'path': ''})
# @tcm_bp.get('/<path:path>/')
def index(path):
    return render_template('tcm/index.html')
