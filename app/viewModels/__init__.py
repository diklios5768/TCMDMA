# -*- encoding: utf-8 -*-
"""
@File Name      :   flask.py
@Create Time    :   2021/7/12 14:00
@Description    :   用于原始数据库模型向视图模型进行转换，提供更好的API，利于复用
@Version        :
@License        :
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from sqlalchemy import and_, or_

from app.libs.error_exception import DataFormatError, NoDataError, DatabaseOperationError
from app.models import db


# from app.utils.hashids import encode_raw_id, decode_hashed_id


# todo:定义数据库操作失败的错误类型和错误状态码
# todo:为id加上hashids操作，1.0版本就不更新了
# attention:此处的通用操作都返回的是查询对象，而不是dict后的字典，方便其他视图函数进行fields设置
def database_add_single(row=None, database_class=None):
    with db.auto_commit():
        if row is not None and database_class is not None:
            new_class = database_class()
            new_class.set_attrs(attrs_dict=row)
            db.session.add(new_class)
        else:
            print(row)
            raise NoDataError()
    return new_class


# 更新数据
def database_update_single(data=None, database_class=None):
    """
    data={
    id:str,
    update_data={}
    }
    """
    with db.auto_commit():
        class_id = data.get("id", None)
        if class_id is not None and database_class is not None:
            row = database_class.query.filter_by(id=class_id).first_or_404()
            row.set_attrs(attrs_dict=data.get("update_data", None))
        else:
            raise NoDataError()


# 假删除数据
def database_remove_single(class_id=None, database_class=None):
    with db.auto_commit():
        if class_id is not None and database_class is not None:
            row = database_class.query.filter_by(id=class_id).first_or_404()
            row.remove()
        else:
            raise NoDataError()


# 恢复数据
def database_recover_single(class_id=None, database_class=None):
    with db.auto_commit():
        if class_id is not None and database_class is not None:
            row = database_class.query.filter_by(id=class_id).first_or_404()
            row.recover()
        else:
            raise NoDataError()


# 从回收站删除数据
def database_delete_single(class_id=None, database_class=None):
    with db.auto_commit():
        if class_id is not None and database_class is not None:
            row = database_class.query.filter_by(id=class_id).first_or_404()
            row.delete(row)
        else:
            raise NoDataError()


# 真从数据库删除数据，管理员访问
def database_true_delete_single(class_id=None, database_class=None):
    with db.auto_commit():
        if class_id is not None and database_class is not None:
            row = database_class.query.filter_by(id=class_id).first_or_404()
            db.session.delete(row)
        else:
            raise NoDataError()


def database_read_by_id_single(class_id=None, database_class=None):
    if class_id is not None and database_class is not None:
        row = database_class.query.filter_by(id=class_id).first_or_404()
        return row
    else:
        raise NoDataError()


def database_read_by_params(database_class=None, filters_by: dict or None = None, join: list or None = None,
                            filters_and: list or None = None, filters_or: list or None = None):
    if database_class is not None:
        rows = database_class.query
        if filters_by:
            rows = rows.filter_by(**filters_by)
        if join:
            rows.join(*join)
        if filters_and:
            rows = rows.filter(and_(*filters_and))
        if filters_or:
            rows = rows.filter(or_(*filters_or))
        return rows.all()
    else:
        raise NoDataError()


def database_read_by_pagination(current_page=None, page_size=None, database_class=None):
    """
    error_out 设为True表示页数不是int或超过总页数时,会报错,并返回404状态码。 默认True
error_out设为False,页数不合法时会返回空列表
    """
    if current_page is not None and page_size is not None and database_class is not None:
        paginate_rows = database_class.query.filter_by().paginate(page=current_page, per_page=page_size, error_out=True,
                                                                  max_per_page=100)
        return paginate_rows
    else:
        raise NoDataError()


# 多次操作
def database_operation_batch(rows: list = None, database_class=None, operation_type: str = ''):
    results = []
    if isinstance(rows, list):
        for row in rows:
            if operation_type in ["add", "create"]:
                results.append(database_add_single(row, database_class))
            elif operation_type == 'update':
                database_update_single(row, database_class)
            elif operation_type == 'remove':
                database_remove_single(row, database_class)
            elif operation_type == 'recover':
                database_recover_single(row, database_class)
            elif operation_type == 'delete':
                database_delete_single(row, database_class)
            elif operation_type == 'true_delete':
                database_true_delete_single(row, database_class)
            elif operation_type in ['search', 'find', 'read', 'get']:
                results.append(database_read_by_id_single(row, database_class))
            else:
                raise DatabaseOperationError()
    else:
        raise DataFormatError()
    return results
