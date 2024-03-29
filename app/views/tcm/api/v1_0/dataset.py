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

from app.libs.error_exception import ReadSuccess, CreateSuccess, UpdateSuccess, TrueDeleteSuccess
from app.models.tcm.dataset import Dataset
from app.models.tcm.user import User
from app.utils.file_handler.table_handler import read_table_to_dataset_data
from app.utils.token_auth import auth
from app.viewModels import database_add_single, database_update_single, database_remove_single, database_recover_single, \
    database_delete_single, database_true_delete_single, database_read_by_id_single, database_operation_batch, \
    database_read_by_params, \
    database_read_by_pagination
from app.viewModels.common.params import params_fuzzy_query, params_remove_pagination, params_remove_empty, \
    params_status, params_antd_table_return
from app.viewModels.tcm.user import is_common_user

dataset_bp = Blueprint('dataset', __name__)


@dataset_bp.get('/all')
@auth.login_required
def get_all_datasets():
    token_info = g.token_info
    user_id = token_info.uid
    datasets = Dataset.query.filter_by(owner_id=user_id).all()
    rows = [dict(dataset) for dataset in datasets]
    rows.reverse()
    return ReadSuccess(data=rows)


@dataset_bp.get('/all_count')
@auth.login_required
def get_all_datasets_count():
    token_info = g.token_info
    user_id = token_info.uid
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
    token_info = g.token_info
    params_dict = request.get_json()
    filters_or = params_fuzzy_query(Dataset, params_remove_empty(params_remove_pagination(params_dict)))
    datasets = database_read_by_params(Dataset, filters_by={'owner_id': token_info.uid, 'status': 1},
                                       filters_or=filters_or)
    dataset_rows = params_antd_table_return(datasets)
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
    token_info = g.token_info
    uid = token_info.uid
    upload_data = request.get_json()
    # print(upload_data)
    file_path = upload_data.get('filePath', "")
    has_header = upload_data.get('hasHeader', False)
    data = read_table_to_dataset_data(file_path=file_path, has_header=has_header)
    row = {"owner_id": uid, "name": upload_data.get("name", None), "description": upload_data.get("description", "无"),
           "data": data, "raw_files_path": [file_path]}
    database_add_single(row, Dataset)
    return CreateSuccess()


# 更新部分信息
@dataset_bp.put('/<int:dataset_id>')
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
@auth.login_required
def remove_dataset_by_id_batch():
    dataset_id_list = request.get_json()
    print(dataset_id_list)
    database_operation_batch(dataset_id_list, Dataset, operation_type='remove')
    return UpdateSuccess(msg='batch remove success', chinese_msg='批量移除成功')


# 从回收站恢复
@dataset_bp.patch('/recover/<int:dataset_id>')
@auth.login_required
def recover_dataset_by_id(dataset_id):
    database_recover_single(dataset_id, Dataset)
    return UpdateSuccess(msg='recover success', chinese_msg='恢复成功')


@dataset_bp.patch('/recover/batch')
@auth.login_required
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
@auth.login_required
def delete_dataset_by_id_batch():
    dataset_id_list = request.get_json().get('idList')
    database_operation_batch(dataset_id_list, Dataset, operation_type='delete')
    return UpdateSuccess(msg='batch delete success', chinese_msg='批量删除成功')


@dataset_bp.post('/admin_params')
@auth.login_required
def get_dataset_by_params_by_admin():
    params_dict = request.get_json()
    filters_and = params_status(Dataset, 1)
    filters_or = []
    if params_dict.get('username', ''):
        username = params_dict.pop('username')
        filters_and.append(Dataset.owner_id == User.id)
        filters_or.append(User.username.like("%{}%".format(username)))
    filters_or.extend(params_fuzzy_query(Dataset, params_remove_empty(params_remove_pagination(params_dict))))
    datasets = database_read_by_params(Dataset, join=[User], filters_and=filters_and, filters_or=filters_or)
    dataset_rows = []
    for dataset in datasets:
        if is_common_user(dataset.user):
            dataset.create_time *= 1000
            dataset_row = dict(dataset)
            dataset_row['key'] = dataset_row['id']
            dataset_row['username'] = dataset.user.username
            dataset_rows.append(dataset_row)
    dataset_rows.reverse()
    return ReadSuccess(data=dataset_rows)


# attention:真删除必须是超级管理员才能用，普通管理员无此权限
@dataset_bp.delete('/true_delete/<int:dataset_id>')
@auth.login_required
def true_delete_dataset(dataset_id):
    database_true_delete_single(dataset_id, Dataset)
    return TrueDeleteSuccess()


@dataset_bp.delete('/true_delete/batch')
@auth.login_required
def true_delete_dataset_batch():
    dataset_id_list = request.get_json()
    database_operation_batch(dataset_id_list, Dataset, operation_type='delete')
    return TrueDeleteSuccess(msg='batch true delete success', chinese_msg='批量真删除成功')
