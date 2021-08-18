from xlrd import open_workbook
from app.libs.error_exception import ParameterException


def read_xls(file_path_or_stream, method='path', row_limit: int = None, col_limit: int = None):
    if method == 'path':
        wb = open_workbook(filename=file_path_or_stream)
    elif method == 'stream':
        wb = open_workbook(file_contents=file_path_or_stream)
    else:
        raise ParameterException()
    ws = wb.sheet_by_index(0)
    table_data = []
    rows_num = ws.nrows
    if row_limit is not None:
        rows_num = row_limit
    for i in range(rows_num):
        if col_limit is not None:
            table_data.append(ws.row_values(i)[0:col_limit])
        else:
            table_data.append(ws.row_values(i))
    return table_data
