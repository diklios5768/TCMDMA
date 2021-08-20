from flask import Blueprint, render_template,current_app,jsonify

from app.views.api import api_bp

# 第一个参数是蓝图的名称，第二个参数是蓝图位置信息
tcm_bp = Blueprint('sun', __name__)
tcm_bp.register_blueprint(api_bp, url_prefix='/sun/api')


@tcm_bp.get('/', defaults={'path': ''})
# @tcm_bp.get('/<path:path>/')
def index(path):
    return render_template('index.html')
