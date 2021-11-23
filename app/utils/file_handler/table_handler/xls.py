from xlrd import open_workbook

from app.libs.error_exception import ParameterException
from app.utils.file_handler.text_handler.list import filter_empty_text


def read_xls(file_path_or_stream, method='path', sheet_name: str = '', sheet_index: int = 0,
             row_start: int = None, row_end: int = None,
             col_start: int = None, col_end: int = None, ):
    if method == 'path':
        wb = open_workbook(filename=file_path_or_stream)
    elif method == 'stream':
        wb = open_workbook(file_contents=file_path_or_stream)
    else:
        raise ParameterException()
    if sheet_name:
        ws = wb.sheet_by_name(sheet_name)
    else:
        ws = wb.sheet_by_index(sheet_index)
    table_data = []
    rows_num = ws.nrows
    if row_start < rows_num:
        row_start = None
    if row_end > rows_num:
        row_end = None
    for i in range(row_start, row_end):
        row = filter_empty_text(ws.row_values(i)[col_start:col_end])
        if row:
            table_data.append(row)
    return table_data
