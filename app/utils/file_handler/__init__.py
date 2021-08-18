import os
from app.settings import basedir
from app.utils.time import generate_datetime_str


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
    return basedir + '/users/upload/' + str(uid) + '-' + username + '/'


def create_user_data_dir_path(uid, username):
    return basedir + '/users/data/' + str(uid) + '-' + username + '/'


def create_user_project_dir_path(user_data_files_dir, project):
    return user_data_files_dir + generate_datetime_str() + str(project.id) + '-' + project.name + '/'
