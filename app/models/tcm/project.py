from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, JSON, Float
from sqlalchemy.orm import relationship, backref
import random
from app.models.base import Base
from app.utils.random import random_content
from app.libs.dicts import project_default_settings

from app.viewModels.tcm.user import find_user
from app.viewModels import database_operation_batch


class Project(Base):
    # 所有者
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # 项目名称
    name = Column(String(100), nullable=False)
    # 描述
    description = Column(String(400), default='无')
    # 项目类型
    type = Column(String(40), default='')
    # 本项目默认设置
    default_settings = Column(JSON, default=project_default_settings)
    # 项目设置
    settings = Column(JSON, default={})
    # 星标
    star = Column(Boolean, default=False)
    # 是否完成
    finished = Column(Boolean, default=False)
    # 完成进度
    finished_rate = Column(Float, default=0)
    # 其他结果
    other_result = Column(JSON, default={})
    analyses = relationship('Analysis', backref=backref('project'), cascade="all, delete")

    fields = ['id', 'name', 'description', 'finished']

    def set_star(self, star):
        self.star = star
        self.touch()


def fake_projects(count):
    users_random = find_user({'type': 'random', 'count': count / 5})['rows']
    users_length = len(users_random)
    rows = [{
        'owner_id': users_random[random.randint(0, users_length - 1)]['id'],
        'name': 'project name' + random_content(length=8, random_type='str_case'),
        'star': False,
        'type': 'Graph',
    } for i in range(count)]
    database_operation_batch(rows, Project, operation_type='add')
