from flask import Blueprint

from app.views.api import api_bp
from app.views.page import page_bp

# 第一个参数是蓝图的名称，第二个参数是蓝图位置信息
sun_bp = Blueprint('sun', __name__)
sun_bp.register_blueprint(api_bp, url_prefix='/api')
sun_bp.register_blueprint(page_bp, url_prefix='/page')
