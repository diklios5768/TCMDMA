from flask import jsonify, request, Blueprint, g
from app.libs.error_exception import Success, ReadSuccess, CreateSuccess, UpdateSuccess, TrueDeleteSuccess, \
    ParameterException, AuthFailed, \
    ServerError
from app.models import db
from app.models.tcm.user import User
from app.models.tcm.project import Project
from app.models.tcm.dataset import Dataset
from app.models.tcm.analysis import Analysis, Method
from app.viewModels import database_add_single, database_update_single, database_remove_single, database_recover_single, \
    database_delete_single, database_read_by_id_single, database_operation_batch, database_read_by_params, \
    database_read_by_pagination, database_true_delete_single
from app.viewModels.common.params import params_ready
from app.viewModels.tcm.project import find_project
from app.utils.token_auth import auth
from app.utils.algorithm_handler import new_analysis
from app.utils.celery_handler import celery_control
from app.utils.file_handler import make_dir, create_user_data_dir_path, create_user_project_dir_path
from app.utils.file_handler.table_handler import read_table_to_dataset_data

project_bp = Blueprint('project', __name__)


# 管理员使用的通用操作
@project_bp.post('/universal/<operation>')
@auth.login_required
def operation_project(operation):
    data = request.get_json()
    result = {'code': 1, 'msg': 'success'}
    if operation == 'add':
        database_add_single(row=data, database_class=Project)
    elif operation == 'remove':
        class_id = data.get('id', 1)
        database_remove_single(class_id=class_id, database_class=Project)
    elif operation == 'recover':
        class_id = data.get('id', 1)
        database_recover_single(class_id=class_id, database_class=Project)
    elif operation == 'delete':
        class_id = data.get('id', 1)
        database_delete_single(class_id=class_id, database_class=Project)
    elif operation == 'update':
        database_update_single(row=data, database_class=Project)
    elif operation == 'find' or operation == 'search':
        result = find_project(data)
    else:
        return jsonify({'code': -1, 'msg': '没有这种操作'})
    return jsonify(result)


@project_bp.get('/all')
@auth.login_required
def get_all_projects():
    user_info = g.user_info
    user_id = user_info.uid
    projects = Project.query.filter_by(owner_id=user_id).all()
    projects_count = len(projects)
    rows = []
    for project in projects:
        project_row = dict(project)
        rate = project.finished_rate
        project_row['rate'] = int(rate * 100)
        failed_analyses = []
        for analysis in project.analyses:
            status = analysis.analysis_status
            if 'fail' in status or 'error' in status:
                failed_analyses.append(analysis.method)
        if failed_analyses:
            failed_analyses_method = ','.join(failed_analyses)
        else:
            failed_analyses_method = '无'
        project_row["failed_analyses_method"] = failed_analyses_method
        project_row['pdf_download_path'] = project.other_result.get('pdf_download_path', '')
        rows.append(project_row)
    rows.reverse()
    return ReadSuccess(data={"projects": rows, "projects_count": projects_count})


@project_bp.get('/all_count')
@auth.login_required
def get_all_projects_count():
    user_info = g.user_info
    user_id = user_info.uid
    projects = Project.query.filter_by(owner_id=user_id).all()
    projects_count = len(projects)
    return ReadSuccess(data={"projects_count": projects_count})


@project_bp.get('/all/differentiate')
@auth.login_required
def get_all_projects_with_differentiate():
    user_info = g.user_info
    user_id = user_info.uid
    projects = Project.query.filter_by(owner_id=user_id, status=1).all()
    projects_count = len(projects)
    finished_projects = []
    running_projects = []
    for project in projects:
        if project.finished:
            finished_projects.append(dict(project))
        else:
            running_project_row = dict(project)
            rate = project.finished_rate
            running_project_row['rate'] = int(rate * 100)
            running_projects.append(running_project_row)

    finished_projects.reverse()
    running_projects.reverse()
    return ReadSuccess(
        data={"finished_projects": finished_projects, "finished_projects_count": len(finished_projects),
              "running_projects": running_projects, "running_projects_count": len(running_projects),
              "projects_count": projects_count})


@project_bp.get('/<int:project_id>')
@auth.login_required
def get_project_by_id(project_id):
    row = database_read_by_id_single(project_id, Project)
    return ReadSuccess(data=dict(row))


@project_bp.post('/params')
@auth.login_required
def get_project_by_params():
    user_info = g.user_info
    params_dict = request.get_json()
    params_dict['owner_id'] = user_info.uid
    print(params_dict)
    finished = params_dict.get('finished', 'all')
    if finished == 'all':
        params_dict.pop('finished')
    filters_by = params_ready(params_dict)
    projects = database_read_by_params(Project, filters_by=filters_by)
    project_rows = []
    for project in projects:
        # row.create_time *= 1000
        project_row = dict(project)
        # project_row['key']=project_row['id']
        failed_analyses = []
        for analysis in project.analyses:
            status = analysis.analysis_status
            if 'fail' in status or 'error' in status:
                failed_analyses.append(analysis.method)
        if failed_analyses:
            failed_analyses_method = ','.join(failed_analyses)
        else:
            failed_analyses_method = '无'
        project_row['failed_analyses_method'] = failed_analyses_method
        project_row['pdf_download_path'] = project.other_result.get('pdf_download_path', '')
        project_rows.append(project_row)
    project_rows.reverse()
    return ReadSuccess(data=project_rows)


@project_bp.get('/paginate')
@auth.login_required
def get_project_by_paginate():
    data = request.get_json()
    current_page = data.get('current', None)
    page_size = data.get('pageSize', None)
    paginate_rows = database_read_by_pagination(current_page, page_size, Project)
    rows = [dict(row) for row in paginate_rows.items]
    rows.reverse()
    return ReadSuccess(data=rows)


@project_bp.get('/batch')
@auth.login_required
def get_project_batch():
    project_id_list = request.get_json()
    batch_rows = database_operation_batch(project_id_list, Project, 'search')
    rows = [dict(row) for row in batch_rows]
    rows.reverse()
    return ReadSuccess(data=rows)


@project_bp.get('/<int:project_id>/analysis_status')
@auth.login_required
def get_project_analysis_status(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    rate = project.finished_rate
    failed_analyses = []
    for analysis in project.analyses:
        status = analysis.analysis_status
        if 'fail' in status or 'error' in status:
            failed_analyses.append(analysis.method)
    failed_analyses_method = ','.join(failed_analyses)
    if rate == 1:
        return Success(data={'finished': True, 'rate': 100, "failed_analyses_method": failed_analyses_method},
                       msg='project is finished', chinese_msg='项目已经完成')
    else:
        return Success(data={'finished': False, 'rate': int(rate * 100)}, msg='project is unfinished',
                       chinese_msg='项目未完成')


@project_bp.get('/finished')
@auth.login_required
def get_all_projects_finished():
    user_info = g.user_info
    user_id = user_info.uid
    projects = Project.query.filter_by(owner_id=user_id, finished=True).all()
    rows = [dict(project) for project in projects]
    rows.reverse()
    return ReadSuccess(data=rows)


@project_bp.get('/unfinished')
@auth.login_required
def get_all_projects_unfinished():
    user_info = g.user_info
    user_id = user_info.uid
    projects = Project.query.filter_by(owner_id=user_id, finished=False).all()
    rows = [dict(project) for project in projects]
    rows.reverse()
    return ReadSuccess(data=rows)


@project_bp.get('/<int:project_id>/is_multiple')
@auth.login_required
def get_project_is_multiple(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    analyses = project.analyses
    all_count = len(analyses)
    if all_count > 1:
        return ReadSuccess(data={"is_multiple": True}, msg='project is multiple', chinese_msg='项目有多个分析方法')
    else:
        return ReadSuccess(data={"is_multiple": False}, msg='project is not multiple', chinese_msg='项目只有一个分析方法')


@project_bp.get('/<int:project_id>/analyses')
@auth.login_required
def get_project_analyses(project_id):
    user_info = g.user_info
    user_id = user_info.uid
    project = Project.query.filter_by(id=project_id).first_or_404()
    if project.owner_id != user_id:
        return AuthFailed(chinese_msg='你无权访问此项目，因为这不是你的项目')
    if project.finished is not True:
        return ServerError(msg='project is not completed', chinese_msg='项目还未完成，请不要请求分析结果')
    analyses = project.analyses
    analyses_main_data = []
    for analysis in analyses:
        status = analysis.analysis_status
        if 'fail' in status or 'error' in status:
            pass
        else:
            analysis_main_result_data = analysis.main_result_data
            method = Method.query.filter_by(name=analysis.method).first_or_404()
            analysis_main_result_data['method'] = method.name
            analysis_main_result_data['chinese_name'] = method.chinese_name
            analyses_main_data.append(analysis_main_result_data)
    return Success(data=analyses_main_data, msg='read analyses success', chinese_msg='读取分析结果成功')


# 不常用
@project_bp.post('')
@auth.login_required
def add_project():
    row = request.get_json()
    database_add_single(row, Project)
    return CreateSuccess()


# attention:最重要的方法
@project_bp.post('/with_dataset_and_analysis')
@auth.login_required
def add_project_with_dataset_and_analysis():
    user_info = g.user_info
    uid = user_info.uid
    user = User.query.filter_by(id=uid).first_or_404()
    data = request.get_json()
    # print(data)
    project_data = data.get('project_data', None)
    if project_data is None:
        return ParameterException()
    dataset_data = data.get('dataset_data', None)
    if dataset_data is None:
        return ParameterException()
    analysis_data = data.get('analysis_data', None)
    if analysis_data is None:
        return ParameterException()
    # 项目直接添加
    project_row = {'owner_id': uid, 'name': project_data.get('projectName', ''),
                   'description': project_data.get('projectDescription', '')}
    project = database_add_single(project_row, Project)
    # 数据集直接添加,只是前端注意要带上原始文件路径
    dataset_row = {'owner_id': uid, 'name': dataset_data.get('datasetName', ''),
                   'description': dataset_data.get('datasetDescription', '')}
    dataset_upload_method = dataset_data.get('datasetUploadMethod', None)
    if dataset_upload_method is None:
        return ParameterException(msg='', chinese_msg='数据集上传方法参数不存在')
    if dataset_upload_method in ['text', 'file']:
        file_path = dataset_data.get('filePath', "")
        has_header = dataset_data.get('hasHeader', False)
        data = read_table_to_dataset_data(file_path=file_path, has_header=has_header)
        dataset_row['data'] = data
        dataset_row['raw_files_path'] = [file_path]
        dataset = database_add_single(dataset_row, Dataset)
    elif dataset_upload_method == 'exist':
        dataset_id = dataset_data.get('datasetID', None)
        if dataset_id is not None:
            dataset = Dataset.query.filter_by(id=dataset_id).first_or_404()
        else:
            return ParameterException(msg='', chinese_msg='未上传数据集id')
    else:
        return ParameterException(msg='upload method not support', chinese_msg='上传方法不存在')
    # 处理方法和参数
    methods = analysis_data.get('methods', None)
    # methods.extend(methods)
    if methods is not None and methods != []:
        # 创建用户数据文件夹和对应项目文件夹
        user_data_files_dir = create_user_data_dir_path(user.id, user.username)
        user_project_files_dir = create_user_project_dir_path(user_data_files_dir, project)
        if not make_dir(user_project_files_dir):
            return False
        for method in methods:
            analysis_dict_data = {'project_id': project.id, 'dataset_id': dataset.id, 'method': method['name']}
            params = method.get('params', {})
            if params != {}:
                analysis_dict_data['parameters'] = params
            else:
                params = {}
                method_row = Method.query.filter_by(name=method['name']).first_or_404()
                method_default_params = method_row.default_parameters
                for default_params in method_default_params:
                    params[default_params['name']] = default_params['default']
                analysis_dict_data['parameters'] = params
            analysis = database_add_single(analysis_dict_data, Analysis)
            # 调用算法
            task = new_analysis.delay(project.id, user_project_files_dir,
                                      analysis.id, method['name'],
                                      dataset.data['table_data'],
                                      analysis.parameters)
    return CreateSuccess(msg='project create success,please wait completed', chinese_msg='项目创建成功，请等待分析完成')


@project_bp.get('/<int:project_id>/stop')
def stop_project_analyses_by_id(project_id):
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    for analysis in project.analyses:
        celery_task_id = analysis.other_result_data['celery_task_id']
        celery_control.revoke(task_id=celery_task_id, terminate=True)
        with db.auto_commit():
            analysis.analysis_status='analysis stop'
    return Success(msg='stop project success', chinese_msg='停止算法运行成功')


# 更新部分信息
@project_bp.put('/<int:project_id>')
@auth.login_required
def update_project_by_id(project_id):
    update_data = request.get_json()
    database_update_single({"id": project_id, "update_data": update_data}, Project)
    return UpdateSuccess()


# 放入回收站
@project_bp.patch('/remove/<int:project_id>')
@auth.login_required
def remove_project_by_id(project_id):
    database_remove_single(project_id, Project)
    return UpdateSuccess(msg='remove success', chinese_msg='移除成功')


@project_bp.patch('/remove/batch')
def remove_project_by_id_batch():
    project_id_list = request.get_json()
    database_operation_batch(project_id_list, Project, operation_type='remove')
    return UpdateSuccess(msg='batch remove success', chinese_msg='批量移除成功')


# 从回收站恢复
@project_bp.patch('/recover/<int:project_id>')
@auth.login_required
def recover_project_by_id(project_id):
    database_recover_single(project_id, Project)
    return UpdateSuccess(msg='recover success', chinese_msg='恢复成功')


@project_bp.patch('/recover/batch')
def recover_project_by_id_batch():
    project_id_list = request.get_json()
    database_operation_batch(project_id_list, Project, operation_type='recover')
    return UpdateSuccess(msg='batch recover success', chinese_msg='批量恢复成功')


# 从回收站删除
@project_bp.patch('/delete/<int:project_id>')
@auth.login_required
def delete_project_by_id(project_id):
    database_delete_single(project_id, Project)
    return UpdateSuccess(msg='delete success', chinese_msg='删除成功')


@project_bp.patch('/delete/batch')
def delete_project_by_id_batch():
    project_id_list = request.get_json()
    database_operation_batch(project_id_list, Project, operation_type='delete')
    return UpdateSuccess(msg='batch delete success', chinese_msg='批量删除成功')


@project_bp.post('/admin_params')
def get_project_by_params_by_admin():
    params_dict = request.get_json()
    finished = params_dict.get('finished', 'all')
    if finished == 'all':
        params_dict.pop('finished')
    filters_by = params_ready(params_dict)
    projects = database_read_by_params(Project, filters_by=filters_by)
    project_rows = [dict(project) for project in projects]
    project_rows.reverse()
    return ReadSuccess(data=project_rows)


# attention:真删除必须是超级管理员才能用，普通管理员无此权限
@project_bp.delete('/true_delete/<int:project_id>')
@auth.login_required
def true_delete_project(project_id):
    database_true_delete_single(project_id, Project)
    return TrueDeleteSuccess()


@project_bp.delete('/true_delete/batch')
@auth.login_required
def true_delete_project_batch():
    project_id_list = request.get_json()
    database_operation_batch(project_id_list, Project, operation_type='delete')
    return TrueDeleteSuccess(msg='batch true delete success', chinese_msg='批量真删除成功')
