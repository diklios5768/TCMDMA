# -*- encoding: utf-8 -*-
"""
@File Name      :   dataset.py    
@Create Time    :   2021/7/14 18:09
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

import random
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, backref
from app.models.tcm import TCMBase
from app.viewModels.tcm.user import find_user
from app.viewModels import database_operation_batch


class Dataset(TCMBase):
    """
    :data:{
    table_data:[[],...],
    columns:[{},...],
    data_source:[{},...],
    table_width:number,
    has_header:boolean,
    file_path:str
    ...
    }
    """
    _id = Column(BigInteger, primary_key=True, nullable=False, index=True, unique=True)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(100), default='无')
    # 对于数据集的描述介绍
    description = Column(String(400), default='无')
    # 具体转换出来的数据
    data = Column(JSON, default={})
    # 原生数据文件路径
    raw_files_path = Column(JSON, default=[])
    # 星标
    star = Column(Boolean, default=False)
    analyses = relationship('Analysis', backref=backref('dataset'))

    fields = ['id', 'name', 'data', 'description', 'create_time']


def fake_datasets(count):
    users_random = find_user({'type': 'random', 'count': count / 5})['rows']
    users_length = len(users_random)
    rows = [{
        'owner_id': users_random[random.randint(0, users_length - 1)]['id'],
        "name": "dataset" + str(i),
        'data': {},
        'raw_files_path': {},
        'description': 'test,fake dataset',
    } for i in range(count)]
    database_operation_batch(rows, Dataset, operation_type='add')
