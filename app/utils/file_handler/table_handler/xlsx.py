from io import BytesIO
from openpyxl import Workbook, load_workbook
from app.settings import basedir
from app.libs.error_exception import ParameterException, ServerError
from app.utils.file_handler import make_dir
from app.utils.file_handler.text_handler.list import filter_empty_text



def read_xlsx(file_path_or_stream, method='path', row_limit: int = None, col_limit: int = None):
    if method == 'path':
        wb = load_workbook(filename=file_path_or_stream,data_only=True)
    elif method == 'stream':
        wb = load_workbook(filename=BytesIO(file_path_or_stream),data_only=True)
    else:
        raise ParameterException()
    ws = wb.active
    table_data = []
    if row_limit is not None:
        rows = ws[1:row_limit]
    else:
        rows = ws.rows
    for row in rows:
        row_data = []
        if col_limit is not None:
            col = row[0:col_limit]
        else:
            col = row
        for j in col:
            if j.value:
                row_data.append(j.value)
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
