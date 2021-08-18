import os
from io import BytesIO
from zipfile import ZipFile


def zip_dir(zip_file_path,files_dir):
    with ZipFile(zip_file_path,'w') as zf:
        # pre_len = len(os.path.dirname(files_dir))
        # for parent, dirnames, filenames in os.walk(files_dir):
        #     for filename in filenames:
        #         pathfile = os.path.join(parent, filename)
        #         relative_path = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
        #         zf.write(pathfile, relative_path)
        # 第二种写法
        for path, dirnames, filenames in os.walk(files_dir):  # 遍历文件
            relative_path = path.replace(files_dir, "")  # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩（即生成相对路径）
            for filename in filenames:
                zf.write(os.path.join(path, filename), os.path.join(relative_path, filename))
    return True


def zip_files(zip_file_path, files):
    try:
        with ZipFile(zip_file_path, 'w') as zf:
            for file in files:
                zf.write(file['path'], file['name'])
        return True
    except FileExistsError as e:
        print('FileExistsError' + str(e))
        return False
    except FileNotFoundError as e:
        print('FileNotFoundError' + str(e))
        return False


# 压缩但是不保存
def zip_files_to_stream(files):
    try:
        memory_file = BytesIO()
        with ZipFile(memory_file, 'w') as zf:
            zf.write()
            for file in files:
                zf.write(file['path'], file['name'])
        # 将文件对象的读写位置“倒回”到起始位置
        memory_file.seek(0)
        return memory_file
    except FileNotFoundError as e:
        print('FileNotFoundError' + str(e))
        return False
