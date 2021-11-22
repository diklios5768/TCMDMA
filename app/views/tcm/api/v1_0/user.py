from flask import request, Blueprint, g

from app.libs.error_exception import Success, ReadSuccess, UpdateSuccess, TrueDeleteSuccess, ParameterException, \
    AuthFailed
from app.models.tcm.user import User
from app.utils.file_handler.text_handler.format import bool_str_to_boolean
from app.utils.token_auth import auth
from app.viewModels import database_add_single, database_read_by_id_single, database_read_by_params, \
    database_remove_single, database_update_single, database_recover_single, database_delete_single, \
    database_operation_batch, database_true_delete_single
from app.viewModels.common.params import params_remove_pagination, params_remove_empty, params_fuzzy_query
from app.viewModels.tcm.user import count_user_access_level, eliminate_admin_user

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
    users = eliminate_admin_user(users)
    users_list = []
    for user in users:
        user.create_time *= 1000
        row = dict(user.append_fields(['confirmed', 'active']))
        row['key'] = user.id
        users_list.append(row)
    return ReadSuccess(data=users_list, msg='search all success')


@user_bp.get('/count')
@auth.login_required
def get_user_count():
    users = User.query.all()
    return ReadSuccess(data={'users_count': len(users)}, msg='search count success')


@user_bp.post('/params')
@auth.login_required
def get_user_by_params():
    params_dict = request.get_json()
    # print(params_dict)
    filters_by = {'status': 1}
    filters_and = []
    filters_or = []
    if params_dict.get('active', ''):
        active = bool_str_to_boolean(params_dict.pop('active'))
        filters_by['active'] = active
    if params_dict.get('confirmed', ''):
        confirmed = bool_str_to_boolean(params_dict.pop('confirmed'))
        filters_by['confirmed'] = confirmed
    if params_dict.get('username', ''):
        username = params_dict.pop('username')
        filters_and.append(User.username.like("%{}%".format(username)))
    filters_or.extend(params_fuzzy_query(User, params_remove_empty(params_remove_pagination(params_dict))))
    users = database_read_by_params(User, filters_by=filters_by, filters_and=filters_and,filters_or=filters_or)
    users = eliminate_admin_user(users)
    users_list = []
    for user in users:
        user.create_time *= 1000
        row = dict(user.append_fields(['confirmed', 'active']))
        row['key'] = user.id
        users_list.append(row)
    return ReadSuccess(data=users_list)


@user_bp.post('')
@auth.login_required
def add_new_user():
    data = request.get_json()
    database_add_single(data, User)
    return Success(msg='add user success', chinese_msg='添加用户成功')


@user_bp.patch('/set_confirmed_status/<int:user_id>')
@auth.login_required
def update_user_confirmed_status(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first_or_404()
    confirmed = data.get('confirmed', user.confirmed)
    database_update_single({'id': user_id, 'update_data': {'confirmed': confirmed}}, User)
    return UpdateSuccess(msg='set user status success', chinese_msg='设置用户状态成功')


@user_bp.patch('/set_confirmed/<int:user_id>')
@auth.login_required
def update_user_confirmed(user_id):
    database_update_single({'id': user_id, 'update_data': {'confirmed': True}}, User)
    return UpdateSuccess(msg='set user pass success', chinese_msg='设置用户通过成功')


@user_bp.patch('/set_not_confirmed/<int:user_id>')
@auth.login_required
def update_user_not_confirmed(user_id):
    database_update_single({'id': user_id, 'update_data': {'confirmed': False}}, User)
    return UpdateSuccess(msg='set user not pass success', chinese_msg='设置用户未通过成功')


@user_bp.patch('/set_active_status/<int:user_id>')
@auth.login_required
def update_user_active_status(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first_or_404()
    active = data.get('active', user.active)
    database_update_single({'id': user_id, 'update_data': {'active': active}}, User)
    return UpdateSuccess(msg='set user status success', chinese_msg='设置用户状态成功')


@user_bp.patch('/set_active/<int:user_id>')
@auth.login_required
def update_user_active(user_id):
    database_update_single({'id': user_id, 'update_data': {'active': True}}, User)
    return UpdateSuccess(msg='set user pass success', chinese_msg='设置用户通过成功')


@user_bp.patch('/set_not_active/<int:user_id>')
@auth.login_required
def update_user_not_active(user_id):
    database_update_single({'id': user_id, 'update_data': {'active': False}}, User)
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
