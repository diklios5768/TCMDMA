import os
from flask import current_app
from app.utils.time import generate_datetime_str_now


# 没有就创建这个文件夹，有就返回True
def make_dir(make_dir_path):
    path = make_dir_path.strip()
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(str(e))
            return False
    return True


def create_user_upload_dir_path(uid, username):
    # return os.path.join(current_app.config.get('USER_UPLOAD_DIR'), str(uid) + '-' + username + '/')
    return './app/users/upload/' + str(uid) + '-' + username + '/'


def create_user_data_dir_path(uid, username):
    # return os.path.join(current_app.config.get('USER_DATA_DIR'), + str(uid) + '-' + username + '/')
    return './app/users/data/' + str(uid) + '-' + username + '/'


def create_user_project_dir_path(user_data_files_dir, project):
    return user_data_files_dir + generate_datetime_str_now() + '--' + str(project.id) + '-' + project.name + '/'
