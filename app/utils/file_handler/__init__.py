import os
from shutil import copy2, copytree, move, rmtree

from app.utils.time import generate_datetime_str_now


def make_dir(make_dir_path: str) -> bool:
    """
    没有就创建这个文件夹，有就直接返回True
    """
    # 为了防止是WindowsPath而报错，先转换一下
    path = str(make_dir_path).strip()
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


def copy_file(source_file_path, target_path):
    """
    如果目标是目录，使用原文件名，否则使用目标路径的文件名
    """
    if os.path.isfile(source_file_path):
        copy2(source_file_path, target_path)
        return True
    else:
        return False


def copy_dir(source_dir_path, target_dir_path):
    """
    把指定的文件夹连文件夹一起，全部拷贝到新的指定的文件夹（必须是不存在到文件夹，会自动重新创建）
    """
    if os.path.isdir(source_dir_path) and os.path.isdir(target_dir_path):
        copytree(source_dir_path, target_dir_path)
        return True
    else:
        return False


def move_file(source_file_path, target_file_path):
    """
    同复制，如果目标是目录，使用原文件名，否则使用目标路径的文件名
    """
    if os.path.isfile(source_file_path):
        move(source_file_path, target_file_path)
        return True
    else:
        return False


def move_dir(source_dir_path, target_dir_path):
    """
    如果目标是已存在的目录，则 src 会被移至该目录下。 如果目标已存在但不是目录，它可能会被覆盖
    如果是不存在的目录，将直接创建这个目录，再把文件夹中的内容移过去（不是包括文件夹本身的移动）
    """
    if os.path.isdir(source_dir_path) and os.path.isdir(target_dir_path):
        move(source_dir_path, target_dir_path)
        return True
    else:
        return False


def remove_file(file_path):
    """
    有文件就删除文件，没有文件就什么都不做
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False


def remove_dir(dir_path):
    """
    有文件夹，则删除文件夹，如果没有文件，则什么都不做
    """
    if os.path.isdir(dir_path):
        rmtree(dir_path)
        return True
    else:
        return False
