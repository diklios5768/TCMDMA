from flask import Blueprint, render_template, current_app, jsonify, url_for

from app.libs.error_exception import Success
from app.views.api import api_bp

# 第一个参数是蓝图的名称，第二个参数是蓝图位置信息
tcm_bp = Blueprint('sun', __name__)
tcm_bp.register_blueprint(api_bp, url_prefix='/sun/api')


@tcm_bp.get('/', defaults={'path': ''})
# @tcm_bp.get('/<path:path>/')
def index(path):
    return render_template('index.html')


@tcm_bp.get('/test')
def test():
    return Success(msg='test success', chinese_msg='测试成功')
