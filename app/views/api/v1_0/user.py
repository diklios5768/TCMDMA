from flask import request, current_app, Blueprint, jsonify, g
from app.libs.error_exception import Success, ReadSuccess, UpdateSuccess, TrueDeleteSuccess, ParameterException, \
    AuthFailed, NotFound
from app.models.tcm.user import User
from app.viewModels import database_add_single, database_read_by_id_single, database_read_by_params, \
    database_remove_single, database_update_single, database_recover_single, database_delete_single, \
    database_operation_batch, database_true_delete_single
from app.viewModels.tcm.user import count_user_access_level
from app.utils.token_auth import auth

user_bp = Blueprint('user', __name__)
# 绑定数据管理
bound_bp = Blueprint('bound', __name__)
# 密码和账户管理
secret_bp = Blueprint('secret', __name__)

user_bp.register_blueprint(bound_bp, url_prefix='/bound')
user_bp.register_blueprint(secret_bp, url_prefix='/secret')


# 至少是管理员才能访问
@user_bp.get('/<int:user_id>')
@auth.login_required
def get_user(user_id):
    user = database_read_by_id_single(user_id, User)
    return ReadSuccess(data=dict(user), msg='search success')


@user_bp.get('/all')
@auth.login_required
def get_user_all():
    users = User.query.all()
    users_list = [dict(user) for user in users]
    return ReadSuccess(data=users_list, msg='search all success')


@user_bp.get('/count')
@auth.login_required
def get_user_count():
    users = User.query.all()
    return ReadSuccess(data={'users_count': len(users)}, msg='search count success')


@user_bp.get('/params')
@auth.login_required
def get_user_by_params():
    params_dict = request.get_json()
    users = database_read_by_params(User, filters_by=params_dict)
    user_rows = [dict(user) for user in users]
    user_rows.reverse()
    return ReadSuccess(data=user_rows)


@user_bp.post('')
@auth.login_required
def add_new_user():
    data = request.get_json()
    database_add_single(data, User)
    return Success(msg='add user success', chinese_msg='添加用户成功')


@user_bp.patch('/status/<int:user_id>')
@auth.login_required
def update_user_status(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first_or_404()
    status = data.get('status', user.status)
    database_update_single({'id': user_id, 'update_data': {'status': status}}, User)
    return UpdateSuccess(msg='set user status success', chinese_msg='设置用户状态成功')


@user_bp.patch('/pass/<int:user_id>')
@auth.login_required
def update_user_status_pass(user_id):
    database_update_single({'id': user_id, 'update_data': {'status': 1}}, User)
    return UpdateSuccess(msg='set user pass success', chinese_msg='设置用户通过成功')


@user_bp.patch('/not_pass/<int:user_id>')
@auth.login_required
def update_user_status_not_pass(user_id):
    database_update_single({'id': user_id, 'update_data': {'status': 0}}, User)
    return UpdateSuccess(msg='set user not pass success', chinese_msg='设置用户未通过成功')


@user_bp.put('/<int:user_id>')
@auth.login_required
def update_user_by_id(user_id):
    update_data = request.get_json()
    database_update_single({"id": user_id, "update_data": update_data}, User)
    return UpdateSuccess()


# 放入回收站
@user_bp.patch('/remove/<int:user_id>')
@auth.login_required
def remove_user_by_id(user_id):
    database_remove_single(user_id, User)
    return UpdateSuccess(msg='remove success', chinese_msg='移除成功')


@user_bp.patch('/remove/batch')
def remove_user_by_id_batch():
    user_id_list = request.get_json()
    database_operation_batch(user_id_list, User, operation_type='remove')
    return UpdateSuccess(msg='batch remove success', chinese_msg='批量移除成功')


# 从回收站恢复
@user_bp.patch('/recover/<int:user_id>')
@auth.login_required
def recover_user_by_id(user_id):
    database_recover_single(user_id, User)
    return UpdateSuccess(msg='recover success', chinese_msg='恢复成功')


@user_bp.patch('/recover/batch')
def recover_user_by_id_batch():
    user_id_list = request.get_json()
    database_operation_batch(user_id_list, User, operation_type='recover')
    return UpdateSuccess(msg='batch recover success', chinese_msg='批量恢复成功')


# 从回收站删除
@user_bp.patch('/delete/<int:user_id>')
@auth.login_required
def delete_user_by_id(user_id):
    database_delete_single(user_id, User)
    return UpdateSuccess(msg='delete success', chinese_msg='删除成功')


@user_bp.patch('/delete/batch')
def delete_user_by_id_batch():
    user_id_list = request.get_json()
    database_operation_batch(user_id_list, User, operation_type='delete')
    return UpdateSuccess(msg='batch delete success', chinese_msg='批量删除成功')


# attention:真删除必须是超级管理员才能用，普通管理员无此权限
@user_bp.delete('/true_delete/<int:user_id>')
@auth.login_required
def true_delete_user(user_id):
    database_true_delete_single(user_id, User)
    return TrueDeleteSuccess()


@user_bp.delete('/true_delete/batch')
@auth.login_required
def true_delete_user_batch():
    user_id_list = request.get_json()
    database_operation_batch(user_id_list, User, operation_type='delete')
    return TrueDeleteSuccess(msg='batch true delete success', chinese_msg='批量真删除成功')


# 修改密码部分
@secret_bp.post('/update_self_password')
@auth.login_required
def update_self_password():
    user_info = g.user_info
    uid = user_info.uid
    data = request.get_json()
    now_password = data.get('now_password', '')
    user = User.query.filter_by(id=uid).first()
    if user.validate_password(now_password):
        new_password = data.get('new_password', '')
        new_password_confirm = data.get('new_password_confirm', '')
        if new_password != new_password_confirm:
            return ParameterException(msg='two password different', chinese_msg='两次密码不一致')
        user.set_password(new_password)
        return Success(msg='modify password success', chinese_msg='修改密码成功')
    else:
        return ParameterException(msg='now password error', chinese_msg='原密码错误')


@secret_bp.post('/update_password/<int:be_operated_user_id>')
@auth.login_required
def update_user_password(be_operated_user_id):
    user_info = g.user_info
    uid = user_info.uid
    # 判断是否有权限更改别的用户的密码
    operate_user_access_level = count_user_access_level(uid)
    be_operated_user_access_level = count_user_access_level(be_operated_user_id)
    if operate_user_access_level <= be_operated_user_access_level:
        return AuthFailed(chinese_msg='您无权更改相同或更高级别权限用户的密码')
    # 更改密码
    data = request.get_json()
    new_password = data.get('new_password', '')
    new_password_confirm = data.get('new_password_confirm', '')
    if new_password != new_password_confirm:
        return ParameterException(msg='two password different', chinese_msg='两次密码不一致')
    be_operated_user = User.query.filter_by(id=be_operated_user_id).first_or_404()
    be_operated_user.set_password(new_password)
    return Success(msg='modify password success', chinese_msg='修改密码成功')
