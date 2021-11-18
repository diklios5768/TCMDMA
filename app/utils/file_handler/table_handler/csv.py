from csv import reader, writer
from io import StringIO

import pandas as pd

from app.libs.error_exception import ParameterException
from app.settings import basedir
from app.utils.file_handler.text_handler.list import filter_empty_text


def get_csv_data(file_data, filter_row: bool = False,
                 row_start: int or None = None, row_end: int or None = None,
                 col_start: int or None = None, col_end: int or None = None, ):
    table_data = []
    for row in file_data:
        if filter_row:
            row = filter_empty_text(row)
        if row:
            table_data.append(row)
    table_data = table_data[row_start:row_end][col_start:col_end]
    return table_data


def read_csv(file_path_or_stream, method='path',
             filter_row: bool = False, delimiter: str = ',',
             row_start: int or None = None, row_end: int or None = None,
             col_start: int or None = None, col_end: int or None = None, ):
    if method == 'path':
        with open(file_path_or_stream, 'r', encoding='utf-8') as f:
            csv_file = reader(f, delimiter=delimiter)
            return get_csv_data(csv_file, filter_row=filter_row,
                                row_start=row_start, row_end=row_end,
                                col_start=col_start, col_end=col_end)
    elif method == 'stream':
        csv_file = reader(StringIO(file_path_or_stream.decode('utf-8')), delimiter=delimiter)
        return get_csv_data(csv_file, filter_row=filter_row,
                            row_start=row_start, row_end=row_end,
                            col_start=col_start, col_end=col_end)
    else:
        raise ParameterException()


def generate_csv_file(filename, table_data, file_dir: str = None):
    if file_dir is not None:
        if not file_dir.endswith('/'):
            file_dir += '/'
        with open(file_dir + filename, 'w', newline='', encoding='utf-8-sig') as f:
            csv_file = writer(f)
            csv_file.writerows(table_data)
    else:
        with open(basedir + '/temp/' + filename, 'w', newline='', encoding='utf-8-sig') as f:
            csv_file = writer(f)
            csv_file.writerows(table_data)
    return True


def read_csv_by_pandas(filepath_or_buffer):
    """
    参数参考read_txt_table_by_pandas
    """
    df = pd.read_csv(filepath_or_buffer)
    return df.to_numpy().tolist(), df


def generate_csv_by_pandas(path_or_buf, df: pd.DataFrame):
    return df.to_csv(path_or_buf)
