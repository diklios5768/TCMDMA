# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/7/14 9:53
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

from flask import Blueprint
from app.views.tcm.api.v1_0.login import login_bp
from app.views.tcm.api.v1_0.register import register_bp
from app.views.tcm.api.v1_0.user import user_bp
from app.views.tcm.api.v1_0.project import project_bp
from app.views.tcm.api.v1_0.dataset import dataset_bp
from app.views.tcm.api.v1_0.file import file_bp
from app.views.tcm.api.v1_0.analysis import analysis_bp

v1_0_bp = Blueprint('v1_0', __name__)

v1_0_bp.register_blueprint(login_bp, url_prefix='/login')
v1_0_bp.register_blueprint(register_bp, url_prefix='/register')
v1_0_bp.register_blueprint(user_bp, url_prefix='/user')
v1_0_bp.register_blueprint(project_bp, url_prefix='/project')
v1_0_bp.register_blueprint(dataset_bp, url_prefix='/dataset')
v1_0_bp.register_blueprint(file_bp, url_prefix='/file')
v1_0_bp.register_blueprint(analysis_bp, url_prefix='/analysis')
