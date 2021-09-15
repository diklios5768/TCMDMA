# -*- encoding: utf-8 -*-
"""
@File Name      :   file.py    
@Create Time    :   2021/7/24 14:28
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

import os
from datetime import datetime
from flask import Blueprint, request, send_from_directory, send_file, g, current_app
from app.libs.error_exception import Success, ParameterException, ServerError
from app.models.tcm.user import User
from app.utils.file_handler import make_dir, create_user_upload_dir_path
from app.utils.file_handler.text_handler import texts_to_single_col_table_data_integral_process
from app.utils.file_handler.table_handler import read_table_to_dataset_data, ant_design_table_limit
from app.utils.token_auth import auth
from app.utils.path import decrypt_file_path, divide_dir_file
from app.settings import basedir

file_bp = Blueprint('file', __name__)


@file_bp.get('/single_file_example')
def send_single_file_example():
    return send_from_directory(directory=basedir + '/utils/algorithm_handler/example/',
                               path='single_file_example.zip',
                               as_attachment=True)


@file_bp.get('/multiple_file_example')
def send_multiple_file_example():
    return send_from_directory(directory=basedir + '/utils/algorithm_handler/example/',
                               path='multiple_file_example.zip',
                               as_attachment=True)


@file_bp.get('/get_file_by_path/<path:file_path>')
def send_file_by_path_from_server(file_path):
    return send_file(path_or_file=os.path.join(os.getcwd(), file_path), download_name=os.path.basename(file_path),
                     as_attachment=True)


@file_bp.get('/get_file_by_str/<string:encode_str>')
def send_file_by_str_from_server(encode_str):
    file_path = decrypt_file_path(encode_str)
    file_dir, filename = divide_dir_file(file_path)
    send_from_directory(directory=file_dir, path=filename, as_attachment=True)


@file_bp.post('/read_file_data')
@auth.login_required
def read_file_data():
    # 获取文件信息
    file = request.files.get('file', None)
    if file is not None:
        user_info = g.user_info
        uid = user_info.uid
        user = User.query.filter_by(id=uid).first_or_404()
        # 创建用户上传文件夹
        user_upload_files_dir = create_user_upload_dir_path(uid, user.username)
        filename = file.filename
        file_path = user_upload_files_dir + str(datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")) + '--' + filename
    else:
        raise ParameterException(msg='file is None', chinese_msg='文件不存在，请重新上传')
    if make_dir(user_upload_files_dir):
        # 存文件并读取文件中的数据
        file.save(file_path)
        # 根据是否带表头，将二维数组转化为ant design的表格数据形式
        has_header = request.values.get('hasHeader', default='') == 'true'
        data = read_table_to_dataset_data(file_path=file_path, has_header=has_header, limit=100)
        return Success(data=data)
    else:
        return ServerError()


# 虽然实际上这并不是文件处理，但是基本是在一个form中使用的，所以放在这个模块中
@file_bp.post('/read_text_data')
@auth.login_required
def read_text_data():
    data = request.get_json()
    text = data.get('text', None)
    if text is not None:
        user_info = g.user_info
        uid = user_info.uid
        user = User.query.filter_by(id=uid).first_or_404()
        # 创建用户上传文件夹
        user_upload_files_dir = create_user_upload_dir_path(uid, user.username)
        if make_dir(user_upload_files_dir):
            file_path = user_upload_files_dir + str(
                datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")) + '--' + 'new_text.txt'
            with open(file_path, 'w')as f:
                f.write(text)
        table_data = texts_to_single_col_table_data_integral_process(text)
        # print(table_data)
    else:
        raise ParameterException(msg='text is None', chinese_msg='文本不存在，请重新上传')
    has_header = data.get('hasHeader', True)
    data = ant_design_table_limit(has_header=has_header, table_data=table_data, file_path=file_path, limit=100)
    return Success(data=data)
