from datetime import datetime

from app.models.tcm.user import User
from app.utils.file_handler.text_handler.encrypt import encrypt_by_cryptography, decrypt_by_cryptography
from app.utils.time import generate_datetime_timestamp_now


def find_user(data):
    users = None
    find_type = data.get('type', 'all')
    # 查看某个用户
    if find_type == 'user_name':
        user = User.query.filter_by(username=data['username'],
                                    status=1).first()
    elif find_type == 'phone':
        user = User.query.filter_by(phone=data['phone'],
                                    status=1).first()
    elif find_type == 'email':
        user = User.query.filter_by(email=data['email'],
                                    status=1).first()
    elif find_type == 'single':
        user = User.query.filter_by(id=data.get('id', 1),
                                    status=1).first()
    elif find_type == 'random':
        users = User.query.filter_by(status=1).limit(data.get('count', 5)).all()
    # 查询已经删除的用户
    elif find_type == 'remove':
        users = User.query.filter_by(status=0).all()
    elif find_type == 'all':
        users = User.query.filter_by(status=1).all()
    else:
        return {'code': -1, 'msg': '查询类型错误'}
    if users is not None:
        users_dict = [dict(single_user) for single_user in users]
    else:
        users_dict = [dict(user)]
    return {'rows': users_dict, 'code': 1, 'msg': '查询成功'}


# 是否是普通用户
def is_common_user(user):
    common_user = True
    for role in user.roles:
        if role.access_level >= 80:
            common_user = False
            break
    return common_user


# 是否是管理员用户
def is_user_admin(user):
    user_admin = False
    for role in user.roles:
        if role.access_level >= 80:
            user_admin = True
            break
    return user_admin


# 去除管理员用户
def eliminate_admin_user(users):
    users_list = []
    for user in users:
        common_user = True
        for role in user.roles:
            if role.access_level >= 80:
                common_user = False
                break
        if common_user:
            users_list.append(user)
    return users_list


# 获取用户最高权限
def count_user_access_level(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    user_access_level = 1
    for role in user.roles:
        if role.access_level > user_access_level:
            user_access_level = role.access_level
    return user_access_level


# 以下是用户用的链接
# 生成链接
def generate_user_link(user_id, secret_key, use='register'):
    datetime_now = generate_datetime_timestamp_now()
    link_str = str(datetime_now) + '--' + str(user_id) + '--' + str(use)
    encrypt_link = encrypt_by_cryptography(link_str, secret_key)
    return encrypt_link


# 解析链接
def analyse_user_link(encrypt_link, secret_key):
    decrypt_link = decrypt_by_cryptography(encrypt_link, secret_key)
    return decrypt_link.split('--')


# 确认链接有效
def confirm_user_link(datetime_use, use, confirm_use):
    # 用途是否正确
    if use != confirm_use:
        return False
    # 时间是否过期
    datetime_now = datetime.utcnow().timestamp()
    if float(datetime_use) + 1200 >= datetime_now:
        return False
    return True
