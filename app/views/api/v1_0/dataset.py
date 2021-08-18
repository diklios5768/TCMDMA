# -*- encoding: utf-8 -*-
"""
@File Name      :   dataset.py    
@Create Time    :   2021/7/15 15:37
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

from flask import Blueprint, request, g
from app.libs.error_exception import ReadSuccess, CreateSuccess, UpdateSuccess
from app.utils.token_auth import auth
from app.utils.file_handler.table_handler import read_table_to_dataset_data
from app.models.tcm.dataset import Dataset
from app.viewModels import database_add_single, database_update_single, database_remove_single, database_recover_single, \
    database_delete_single, database_read_by_id_single, database_operation_batch, database_read_by_params, \
    database_read_by_pagination
from app.viewModels.common.params import params_ready

dataset_bp = Blueprint('dataset', __name__)


@dataset_bp.get('/all')
@auth.login_required
def get_all_datasets():
    user_info = g.user_info
    user_id = user_info.uid
    datasets = Dataset.query.filter_by(owner_id=user_id).all()
    rows = [dict(dataset) for dataset in datasets]
    rows.reverse()
    return ReadSuccess(data=rows)


@dataset_bp.get('/all_count')
@auth.login_required
def get_all_datasets_count():
    user_info = g.user_info
    user_id = user_info.uid
    datasets = Dataset.query.filter_by(owner_id=user_id).all()
    datasets_count = len(datasets)
    return ReadSuccess(data={"datasets_count": datasets_count})


@dataset_bp.get('/<int:dataset_id>')
@auth.login_required
def get_dataset_by_id(dataset_id):
    row = database_read_by_id_single(dataset_id, Dataset)
    return ReadSuccess(data=dict(row))


@dataset_bp.post('/params')
@auth.login_required
def get_dataset_by_params():
    user_info = g.user_info
    params_dict = request.get_json()
    params_dict['owner_id'] = user_info.uid
    filters_by = params_ready(params_dict)
    rows = database_read_by_params(Dataset, filters_by=filters_by)
    dataset_rows = []
    for row in rows:
        row.create_time *= 1000
        dataset_row = dict(row)
        dataset_row['key'] = dataset_row['id']
        dataset_rows.append(dataset_row)
    dataset_rows.reverse()
    return ReadSuccess(data=dataset_rows)


@dataset_bp.post('/paginate')
@auth.login_required
def get_dataset_by_paginate():
    data = request.get_json()
    current_page = data.get('current', None)
    page_size = data.get('pageSize', None)
    paginate_rows = database_read_by_pagination(current_page, page_size, Dataset)
    rows = [dict(row) for row in paginate_rows.items]
    rows.reverse()
    return ReadSuccess(data=rows)


@dataset_bp.post('/batch')
@auth.login_required
def get_dataset_batch():
    dataset_id_list = request.get_json()
    batch_rows = database_operation_batch(dataset_id_list, Dataset, 'search')
    rows = [dict(row) for row in batch_rows]
    rows.reverse()
    return ReadSuccess(data=rows)


@dataset_bp.post('')
@auth.login_required
def add_dataset():
    user_info = g.user_info
    uid = user_info.uid
    upload_data = request.get_json()
    print(upload_data)
    file_path = upload_data.get('filePath', "")
    has_header = upload_data.get('hasHeader', False)
    data = read_table_to_dataset_data(file_path=file_path, has_header=has_header)
    row = {"owner_id": uid, "name": upload_data.get("name", None), "description": upload_data.get("description", "无"),
           "data": data, "raw_files_path": [file_path]}
    database_add_single(row, Dataset)
    return CreateSuccess()


# 更新部分信息
@dataset_bp.patch('/<int:dataset_id>')
@auth.login_required
def update_dataset_by_id(dataset_id):
    update_data = request.get_json()
    database_update_single({"id": dataset_id, "update_data": update_data}, Dataset)
    return UpdateSuccess()


# 放入回收站
@dataset_bp.patch('/remove/<int:dataset_id>')
@auth.login_required
def remove_dataset_by_id(dataset_id):
    database_remove_single(dataset_id, Dataset)
    return UpdateSuccess(msg='remove success', chinese_msg='移除成功')


@dataset_bp.patch('/remove/batch')
def remove_dataset_by_id_batch():
    dataset_id_list = request.get_json()
    database_operation_batch(dataset_id_list, Dataset, operation_type='remove')
    return UpdateSuccess(msg='batch remove success', chinese_msg='批量移除成功')


# 从回收站恢复
@dataset_bp.patch('/recover/<int:dataset_id>')
@auth.login_required
def recover_dataset_by_id(dataset_id):
    database_recover_single(dataset_id, Dataset)
    return UpdateSuccess(msg='recover success', chinese_msg='恢复成功')


@dataset_bp.patch('/recover/batch')
def recover_dataset_by_id_batch():
    dataset_id_list = request.get_json().get('idList')
    database_operation_batch(dataset_id_list, Dataset, operation_type='recover')
    return UpdateSuccess(msg='batch recover success', chinese_msg='批量恢复成功')


# 从回收站删除
@dataset_bp.patch('/delete/<int:dataset_id>')
@auth.login_required
def delete_dataset_by_id(dataset_id):
    database_delete_single(dataset_id, Dataset)
    return UpdateSuccess(msg='delete success', chinese_msg='删除成功')


@dataset_bp.patch('/delete/batch')
def delete_dataset_by_id_batch():
    dataset_id_list = request.get_json().get('idList')
    database_operation_batch(dataset_id_list, Dataset, operation_type='delete')
    return UpdateSuccess(msg='batch delete success', chinese_msg='批量删除成功')
