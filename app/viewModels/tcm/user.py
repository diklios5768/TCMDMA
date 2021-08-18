from app.models.tcm.user import User


def find_user(data):
    users=None
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
