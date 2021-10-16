from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.models.user import BaseUser, BaseRole
from app.models.manage import BaseLog
from app.models import db

# todo:以后考虑用户分组功能

user_role = db.Table(
    'user_role',
    Column('user_id', Integer, ForeignKey('user.id')),
    # 级联删除
    Column('role_id', Integer, ForeignKey('role.id')),
)


class User(BaseUser):
    projects = relationship('Project', backref=backref('user'), cascade="all, delete")
    datasets = relationship('Dataset', backref=backref('user'))
    # 级联删除
    # api = db.relationship('Api', backref='project', cascade="all, delete-orphan")
    # api = db.relationship('Api', backref='project', cascade="all, delete")
    roles = relationship('Role', secondary=user_role, backref=backref('users', lazy='dynamic'))
    logs = relationship('UserLog', backref=backref('user'), cascade="all, delete")
    # groups = relationship('Group', secondary=user_group, backref=backref('users', lazy='dynamic'))

    fields = ['id', 'username', 'email', 'phone', 'create_time', 'modify_time']


# 用户角色
class Role(BaseRole):
    pass


# 用户日志
class UserLog(BaseLog):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)


def init_role():
    with db.auto_commit():
        user = Role()
        user.set_attrs({'name': '普通用户', 'access_level': 1})
        db.session.add(user)
        admin = Role()
        admin.set_attrs({'name': '管理员', 'access_level': 2})
        db.session.add(admin)
        super_admin = Role()
        super_admin.set_attrs({'name': '超级管理员', 'access_level': 3})
        db.session.add(super_admin)


def init_user():
    with db.auto_commit():
        # 测试用户
        role_user = Role.query.filter_by(id=1).first_or_404()
        user = User()
        user.set_attrs({'username': 'test', 'email': 'xminer2021@126.com', 'status': 1})
        user.set_password('test1234')
        user.roles.append(role_user)
        db.session.add(user)
        # 管理员
        role_admin = Role.query.filter_by(id=2).first_or_404()
        admin_user = User()
        admin_user.set_attrs({'username': 'admin', 'status': 1})
        admin_user.set_password('admin')
        admin_user.roles.append(role_admin)
        db.session.add(admin_user)
        # 超级管理员
        role_super_admin = Role.query.filter_by(id=3).first_or_404()
        super_admin_user = User()
        super_admin_user.set_attrs({'username': 'super admin', 'status': 1})
        super_admin_user.set_password('super admin')
        super_admin_user.roles.append(role_super_admin)
        db.session.add(super_admin_user)


# 假用户应该是各种权限的用户各一个，普通用户可以很多个
def fake_users(count):
    with db.auto_commit():
        # 普通用户
        role_user = Role.query.filter_by(id=1).first_or_404()
        for i in range(count):
            user = User()
            user.set_attrs({'username': 'user' + str(i)})
            user.set_password('password' + str(i))
            user.roles.append(role_user)
            db.session.add(user)
    init_user()
