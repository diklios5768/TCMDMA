import random

from sqlalchemy import Column, Integer, BigInteger, String, JSON, ForeignKey

from app.libs.lists import analysis_methods
from app.models import db
from app.models.base import Base
from app.viewModels import database_operation_batch
from app.viewModels.tcm.dataset import find_dataset
from app.viewModels.tcm.project import find_project


class Analysis(Base):
    """
    因为为了防止以后出现一个项目对应多个数据集的这种多对多需求，所以改为了这种以一次分析为核心的模式
    """
    id = Column(BigInteger, primary_key=True, nullable=False, index=True, unique=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    dataset_id = Column(BigInteger, ForeignKey('dataset.id'), nullable=False)
    method = Column(String(50), default='无')
    parameters = Column(JSON, default={})
    main_result_data = Column(JSON, default={})
    other_result_data = Column(JSON, default={})
    analysis_status = Column(String(50), default='wait to start')
    fields = ['id', 'project_id', 'dataset_id', 'method', 'main_result_data', 'other_result_data', 'analysis_status']


def fake_analyses(count):
    projects_random = find_project({'type': 'random', 'count': count / 5})['rows']
    projects_length = len(projects_random)
    datasets_random = find_dataset({'type': 'random', 'count': count / 5})['rows']
    datasets_length = len(datasets_random)
    rows = [{
        'project_id': projects_random[random.randint(0, projects_length - 1)]['id'],
        'dataset_id': datasets_random[random.randint(0, datasets_length - 1)]['id'],
        'method': '',
        'main_result_data': {},
        'other_result_data': {},
        'analysis_status': 'wait to start',
    } for i in range(count)]
    database_operation_batch(rows, Analysis, operation_type='add')


class Method(Base):
    """
    :default_parameters:[{
    name:str,
    chinese_name:str,
    default:number,
    step:number
    },...]
    """
    name = Column(String(50), unique=True)
    chinese_name = Column(String(100), unique=True)
    default_parameters = Column(JSON, default=[])
    parameters_introduction = Column(JSON, default=[])
    simple_description = Column(String(100), default='无')
    detail = Column(JSON, default=[])
    description_image = Column(String(200), default='无')
    limits = Column(JSON, default={})

    fields = [
        'id', 'name', 'chinese_name', 'default_parameters', 'parameters_introduction', 'simple_description', 'detail',
        'description_image'
    ]


def init_method():
    database_operation_batch(analysis_methods, Method, operation_type='add')


def update_method():
    with db.auto_commit():
        for index, method_data in enumerate(analysis_methods):
            method = Method.query.filter_by(id=index).first()
            if method:
                method.set_attrs(method_data)
            else:
                method = Method()
                method.set_attrs(method_data)
                db.session.add(method)
