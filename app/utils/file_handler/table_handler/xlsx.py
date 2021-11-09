from io import BytesIO

from openpyxl import Workbook, load_workbook

from app.libs.error_exception import ParameterException, ServerError
from app.settings import basedir
from app.utils.file_handler import make_dir


def read_xlsx(file_path_or_stream, sheet_name: str = '', method='path',
              row_start: int or None = None,row_end: int or None = None,
              col_start: int or None = None, col_end: int or None = None, ):
    """
    注意：start一定要比end小1，否则读出来是空数组
    """
    if method == 'path':
        wb = load_workbook(filename=file_path_or_stream, data_only=True)
    elif method == 'stream':
        wb = load_workbook(filename=BytesIO(file_path_or_stream), data_only=True)
    else:
        raise ParameterException()
    if sheet_name:
        ws = wb[sheet_name]
    else:
        ws = wb.active
    table_data = []
    rows = ws.rows[row_start:row_end]
    for row in rows:
        row_data = []
        cols = row[col_start:col_end]
        for col in cols:
            if col.value:
                row_data.append(col.value)
            else:
                row_data.append('')
        if row_data:
            table_data.append(row_data)
    return table_data


def generate_xlsx_file(filename, table_sheets, file_dir: str = None):
    wb = Workbook()
    for table_sheet in table_sheets:
        ws = wb.create_sheet(table_sheet['name'])
        table_data = table_sheet['data']
        rows_length = len(table_data)
        for i in range(rows_length):
            col_length = len(table_data[i])
            for j in range(col_length):
                ws.cell(row=i + 1, column=j + 1, value=table_data[i][j])
    wb.remove(wb['Sheet'])
    if file_dir is not None:
        if make_dir(file_dir):
            if not file_dir.endswith('/'):
                file_dir += '/'
            wb.save(file_dir + filename)
        else:
            raise ServerError()
    else:
        wb.save(basedir + '/temp/' + filename)
    return True
