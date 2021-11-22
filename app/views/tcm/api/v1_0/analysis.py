# import os, json
# from io import BytesIO
# from threading import Lock
# from zipfile import ZipFile

from flask import jsonify, request, send_from_directory, send_file, Blueprint
# from flask_socketio import emit, join_room, send
# from app.extensions import socket_io
# from app.settings import basedir
from app.libs.error_exception import ReadSuccess
from app.models.tcm.analysis import Analysis, Method
from app.viewModels import database_add_single, database_remove_single, database_recover_single, database_delete_single, \
    database_update_single, database_read_by_id_single
from app.viewModels.tcm.analysis import find_analysis
# from app.utils.random import random_content
# from app.utils.file_handler.text_handler import texts_to_rows_integral_process
# from app.utils.file_handler.table_handler import read_table
# from app.utils.file_handler.table_handler.xlsx import generate_xlsx_file
# from app.utils.file_handler.pdf_handler.fpdf2_generate import generate_relation_analysis_report
# from app.utils.file_handler.zip_handler import zip_files
# from app.utils.algorithm_handler.data_analysing_mining.relational_analysis import relational_analysis
# from app.utils.algorithm_handler.complex_network import community_discovering_analysis
# from app.utils.mail_handler.base import text_mail, files_mail
from app.utils.token_auth import auth

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.post('/universal/<operation>')
@auth.login_required
def operation_graph(operation):
    data = request.get_json()
    result = {'code': 1, 'msg': 'success'}
    if operation == 'add':
        database_add_single(data=data, database_class=Analysis)
    elif operation == 'remove':
        class_id = data.get('id', 1)
        database_remove_single(class_id=class_id, database_class=Analysis)
    elif operation == 'recover':
        class_id = data.get('id', 1)
        database_recover_single(class_id=class_id, database_class=Analysis)
    elif operation == 'delete':
        class_id = data.get('id', 1)
        database_delete_single(class_id=class_id, database_class=Analysis)
    elif operation == 'update':
        database_update_single(data=data, database_class=Analysis)
    elif operation == 'find' or operation == 'search':
        result = find_analysis(data)
    else:
        return jsonify({'code': -1, 'msg': '没有这种操作'})
    return jsonify(result)


@analysis_bp.get('<int:analysis_id>')
@auth.login_required
def get_analysis_by_id(analysis_id):
    row = database_read_by_id_single(analysis_id, Analysis)
    return ReadSuccess(data=row)


# attention:方法也放这里，不是很需要新开一个模块
@analysis_bp.get('/methods')
def get_all_methods():
    methods = Method.query.filter_by().all()
    methods_rows = []
    for method in methods:
        methods_rows.append(dict(method))
    return ReadSuccess(data=methods_rows)

# @analysis_bp.route('api/add_new_analysis', methods=["GET", "POST"])
# def add_new_analysis():
#     form = request.form
#     data = json.loads(form.get('data', {}))
#     print(data)
#     method = data.get('method', [])
#     rows_list = []
#     # 处理文件
#     if data.get('uploadMethod') == 'file':
#         files = request.files.getlist("files")
#         try:
#             for file in files:
#                 # 先读取文件并存储在内存中
#                 file_read = file.read()
#                 filename = file.filename
#                 if 'complex_network' in method:
#                     upload_file_path = basedir + '/upload/' + filename
#                     with open(upload_file_path, 'wb') as f:
#                         f.write(file_read)
#                 rows = []
#                 # 文本文件直接读取
#                 if filename.endswith(".txt"):
#                     rows_list.append(texts_to_rows_integral_process(file_read.decode('utf-8')))
#                 # 表格文件使用不同的模块读取
#                 elif filename.endswith('.xls'):
#                     rows = read_table_from_stream(file_read, 'xls')
#                 elif filename.endswith('.xlsx'):
#                     rows = read_table_from_stream(file_read, 'xlsx')
#                 elif filename.endswith('.csv'):
#                     rows = read_table_from_stream(file_read, 'csv')
#                 else:
#                     return jsonify({'code': -1, 'msg': '上传的文件中有不支持的格式，请重新上传'})
#                 # 最后处理一下文本数据中不规范的部分
#                 for (index, row) in enumerate(rows):
#                     rows[index] = replace_character(row)
#                 rows_list.append(rows)
#         except UnicodeDecodeError as e:
#             print(e)
#             return jsonify({'code': -1, 'msg': '文件非utf-8编码，请重新上传'})
#     # 处理文本
#     elif data.get('uploadMethod') == 'text':
#         texts = data.get("texts")
#         for text in texts:
#             rows_list.append(texts_to_rows_integral_process(text))
#     # 算法处理
#     if 'associative_analysis' in method:
#         min_support = data.get('min_support', 0.5)
#         min_confidence = data.get('min_confidence', 0.5)
#         tree_data, graph_data, tables_data, pdf_tables, excel_tables = relational_analysis(rows_list[0],
#                                                                                            min_support=min_support,
#                                                                                            min_confidence=min_confidence,
#                                                                                            method=method[1])
#         # add_result=database_add({'type': 'single', 'row': {
#         #     'project_id':data.get('project_id'),
#         #     'dataset_name': data.get('dataset_name'),
#         #     'upload_dataset':rows_list,
#         #     'tables_data':tables_data,
#         #     'graph_data':graph_data,
#         #     'tree_data':tree_data,
#         #     'other_data':data
#         # }},Graph)
#         # graph_id=add_result.id
#         tag_name = 'homogeneous_relation_analysis_report_' + random_content(random_type='str_case', length=12)
#         pdf_name = tag_name + '.pdf'
#         excel_name = tag_name + '.xlsx'
#         zip_name = tag_name + '.zip'
#         generate_relation_analysis_report(tables=pdf_tables, name=pdf_name)
#         generate_excel_result = generate_excel_file(file_name=excel_name, tables=excel_tables)
#         # database_update({'id':graph_id,'update_data':{'other_data':{'pdf_path':pdf_path,'excel_path':excel_path,'zip_path':zip_path}}},Graph)
#     elif 'complex_network' in method:
#         threshold = data.get('threshold')
#         if 'relation' in method:
#             if 'GN' in method:
#                 tree_data, graph_data, tables_data = community_discovering_analysis(upload_file_path, 'traditional',
#                                                                                     'GN', threshold)
#             elif 'louvain' in method:
#                 tree_data, graph_data, tables_data = community_discovering_analysis(upload_file_path, 'traditional',
#                                                                                     'louvain', threshold)
#         elif 'embedding' in method:
#             if 'w2c' in method:
#                 tree_data, graph_data, tables_data = community_discovering_analysis(upload_file_path, 'w2c', 'louvain',
#                                                                                     threshold)
#             elif 'n2c' in method:
#                 if 'with_att' in method:
#                     tree_data, graph_data, tables_data = community_discovering_analysis(upload_file_path, 'n2c-att',
#                                                                                         'louvain', threshold)
#                 elif 'without_att' in method:
#                     tree_data, graph_data, tables_data = community_discovering_analysis(upload_file_path,
#                                                                                         'n2c-without-att', 'louvain',
#                                                                                         threshold)
#
#     if data.get('graph', False):
#         return_content = {"code": 1, 'msg': 'success', 'tables_data': tables_data, 'graph_data': graph_data,
#                           'tree_data': tree_data}
#     if data.get('pdf', False):
#         return_content['pdf_name'] = pdf_name
#     if data.get('download', False):
#         return_content['download'] = True
#     if data.get('send', False):
#         try:
#             email = data.get('email', '1061995104@qq.com')
#             print(email)
#             print(type(email))
#             if generate_excel_result and zip_files(basedir + '/static/zips/' + zip_name,
#                                                    [{'path': basedir + '/static/pdf/' + pdf_name,
#                                                      'file_name': pdf_name},
#                                                     {'path': basedir + '/static/tables/' + excel_name,
#                                                      'file_name': excel_name}]) is True:
#                 files_mail('分析报告', [email], '分析报告包括了简要PDF报告文件和详细Excel报告文件',
#                            '<h1>分析报告包括了简要PDF报告文件和详细Excel报告文件<h1/>',
#                            files=[{'path': basedir + '/static/zips/' + zip_name, 'name': zip_name,
#                                    'content_type': 'application/zip'}])
#         except Exception as e:
#             print('Exception ' + str(e))
#             return jsonify({'code': -1, 'msg': 'Fail,please try again' + str(e)})
#     return jsonify(return_content)

# thread = None
# thread_lock = Lock()
#
# @socket_io.on('join', namespace='/user_ws')
# def on_join(message):
#     projectID = message['projectID']
#     join_room(projectID)
#     send('join room ' + projectID, room=projectID)
#
#
# @socket_io.on('get_analysing_list', namespace='/user_ws')
# def get_analysing_list(message):
#     projectID = message['projectID']
#     room = projectID
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socket_io.start_background_task(target=background_get_analysing_list(projectID, room))
#     print(message)
#
#
# def background_get_analysing_list(projectID, room):
#     analysing_list = []
#     while True:
#         db_analysing_list = find_analysis({'type': 'analysing', 'projectID': projectID})
#         for i in db_analysing_list:
#             process = 0
#             processStatus = 'analysing'
#             if i.analysisStatus == 'get dataset':
#                 process = 0
#             elif i.analysisStatus == 'verifying dataset':
#                 process = 10
#             elif i.analysisStatus == 'dataset error':
#                 process = 30
#                 processStatus = 'fail'
#             elif i.analysisStatus == 'analysing':
#                 process = 30
#             elif i.analysisStatus == 'analysis fail':
#                 process = 80
#                 processStatus = 'fail'
#             elif i.analysisStatus == 'analysis success':
#                 process = 80
#                 processStatus = 'success'
#             elif i.analysisStatus == 'generate pdf':
#                 process = 100
#                 processStatus = 'success'
#             analysing_list.append(
#                 {'analysisID': i.analysisID, 'analysisName': i.projectName, 'analysisStatus': i.analysisStatus,
#                  'process': process, 'processStatus': processStatus})
#         emit('send_analysing_list', {'data': analysing_list}, namespace='/user_ws', room=room)  # 发送数据
#         # 每5秒查询并发送一次
#         socket_io.sleep(5)
