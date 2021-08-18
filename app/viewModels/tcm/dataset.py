# -*- encoding: utf-8 -*-
"""
@File Name      :   dataset.py    
@Create Time    :   2021/7/15 15:43
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

# 对项目的增删改查
from app.models.tcm.dataset import Dataset


def find_dataset(data):
    datasets = None
    find_type = data.get('type', 'all')
    owner_id = data.get('owner_id', 1)
    # 查看所有的历史数据集
    if find_type == 'history':
        datasets = Dataset.query.filter_by(owner_id=owner_id,
                                           status=1).all()
    elif find_type == 'single':
        dataset = Dataset.query.filter_by(id=data['project_id'], status=1).first()
    elif find_type == 'random':
        datasets = Dataset.query.filter_by(status=1).limit(data['count']).all()
    # 查询标星的项目
    elif find_type == 'star':
        datasets = Dataset.query.filter_by(owner_id=owner_id,
                                           star=True,
                                           status=1).all()
    # 查询已经删除的数据集
    elif find_type == 'remove':
        datasets = Dataset.query.filter_by(owner_id=owner_id,
                                           status=0).all()
    elif find_type == 'all':
        datasets = Dataset.query.filter_by(status=1).all()
    if datasets is not None:
        datasets_dict = [dict(dataset) for dataset in datasets]
    else:
        datasets_dict = [dict(dataset)]
    return {'rows': datasets_dict, 'code': 1, 'msg': '查询成功'}
