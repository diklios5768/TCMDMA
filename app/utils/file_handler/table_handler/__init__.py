import os
from .csv import read_csv
from .xls import read_xls
from .xlsx import read_xlsx
from app.libs.error_exception import ParameterException
from app.utils.file_handler.text_handler import texts_to_single_col_table_data_integral_process


def read_table(file_path_or_stream, file_type='csv', method='path', row_limit: int = None, col_limit: int = None):
    if file_type == 'csv':
        return read_csv(file_path_or_stream, method, row_limit, col_limit)
    elif file_type == 'xls':
        return read_xls(file_path_or_stream, method, row_limit, col_limit)
    elif file_type == 'xlsx':
        return read_xlsx(file_path_or_stream, method, row_limit, col_limit)
    else:
        raise ParameterException()


def to_ant_design_table_format(table_data, has_header=True):
    if table_data is None or table_data == []:
        raise ParameterException(msg='data is none', chinese_msg='上传的数据都是空字符')
    columns = []
    data_source = []
    table_width = 0
    if has_header:
        table_header = table_data[0]
        table_body = table_data[1:]
        for (index, value) in enumerate(table_header):
            value = str(value)
            columns.append({"title": value, "dataIndex": value, "key": value, "copyable": True,
                            "ellipsis": True, "tip": "内容过长会自动收缩",
                            })
            table_width += len(value)
    else:
        col_len = 0
        for row in table_data:
            this_col_len = len(row)
            if this_col_len > col_len:
                col_len = this_col_len
        table_body = table_data
        table_width = col_len
        for i in range(col_len):
            columns.append(
                {"title": '列' + str(i + 1), "dataIndex": str(i + 1), "key": str(i + 1), "copyable": True,
                 "ellipsis": True,
                 "tip": "内容过长会自动收缩"})
    print(columns)
    for (row_index, row_value) in enumerate(table_body):
        row_dict = {"key": row_index}
        for (col_index, col_value) in enumerate(row_value):
            row_dict[columns[col_index]['dataIndex']] = str(col_value)
        data_source.append(row_dict)
    return columns, data_source, table_width


def ant_design_table_limit(has_header, table_data, file_path, limit: int = None):
    if has_header is not None:
        columns, data_source, table_width = to_ant_design_table_format(table_data, has_header=has_header)
    else:
        raise ParameterException()
    data = {"table_data": table_data, "columns": columns, "file_path": file_path,
            "table_width": table_width, "has_header": has_header}
    if limit is not None:
        if len(data_source) >= limit:
            data["data_source"] = data_source[0:limit]
        else:
            data["data_source"] = data_source
    else:
        data["data_source"] = data_source
    return data


def read_table_to_dataset_data(file_path: str, has_header: bool, limit: int = None):
    filename = os.path.basename(file_path)
    if filename.endswith('.txt'):
        with open(file_path, 'r', encoding='utf8') as file_open:
            file_read = file_open.read()
            table_data = texts_to_single_col_table_data_integral_process(file_read)
    elif filename.endswith('.xls'):
        table_data = read_table(file_path, file_type='xls', method='path')
    elif filename.endswith('.xlsx'):
        table_data = read_table(file_path, file_type='xlsx', method='path')
    elif filename.endswith('.csv'):
        table_data = read_table(file_path, file_type='csv', method='path')
    else:
        return ParameterException(msg='file type error', chinese_msg='文件格式不支持，请重新上传')
    data = ant_design_table_limit(has_header=has_header, table_data=table_data, file_path=file_path, limit=limit)
    return data
