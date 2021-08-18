from flask import request, current_app, Blueprint, jsonify, g

from app.models.tcm.user import User

from app.utils.token_auth import auth
from app.libs.error_exception import NotFound

user_bp = Blueprint('user', __name__)
# 绑定数据管理
bound_bp = Blueprint('bound', __name__)
# 密码和账户管理
secret_bp = Blueprint('secret', __name__)

user_bp.register_blueprint(bound_bp, url_prefix='/bound')
user_bp.register_blueprint(secret_bp, url_prefix='/secret')


# todo:用户管理
# 至少是管理员才能访问


@user_bp.get('/<int:uid>')
@auth.login_required
def get_user(uid):
    user = User.query.get_or_404(id=uid)
    return jsonify(user)


@user_bp.delete('/')
@auth.login_required
def delete_user():
    uid = g.user.uid
    user = User.query.get_or_404(id=uid)
    return jsonify(user)
