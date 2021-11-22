from flask import Blueprint, render_template, redirect, url_for

from app.libs.error_exception import Success
from app.utils.limiter import test_limiter
from app.views.tcm import tcm_bp

main_bp = Blueprint('main', __name__)
main_bp.register_blueprint(tcm_bp, url_prefix='/sun')


@main_bp.get('/')
@main_bp.get('/index')
def index():
    return redirect(url_for('main.tcm.index'))


@main_bp.get('/404')
def not_found():
    return render_template('base/404.html')


@main_bp.get('/test')
@test_limiter
def test():
    return Success(msg='test success', chinese_msg='测试成功')
