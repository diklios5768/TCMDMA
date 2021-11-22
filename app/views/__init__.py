from flask import Blueprint

from app.libs.error_exception import Success
from app.utils.limiter import test_limiter
from app.views.tcm import tcm_bp

index_bp = Blueprint('index', __name__)
index_bp.register_blueprint(tcm_bp, url_prefix='/sun')


@index_bp.get('/test')
@test_limiter
def test():
    return Success(msg='test success', chinese_msg='测试成功')
