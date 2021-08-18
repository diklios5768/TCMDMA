from io import StringIO
from csv import reader, writer
from app.libs.error_exception import ParameterException
from app.settings import basedir


def get_csv_data(file, row_limit: int = None, col_limit: int = None):
    table_data = []
    for row in file:
        table_data.append(row)
    if row_limit is not None:
        if col_limit is not None:
            table_data = table_data[0:row_limit][0:col_limit]
        else:
            table_data = table_data[0:row_limit]
    else:
        if col_limit is not None:
            table_data = table_data[:][0:col_limit]
        else:
            table_data = table_data[:]
    return table_data


def read_csv(file_path_or_stream, method='path', row_limit: int = None, col_limit: int = None):
    if method == 'path':
        with open(file_path_or_stream, 'r', encoding='utf-8') as f:
            csv_file = reader(f)
            return get_csv_data(csv_file, row_limit=row_limit, col_limit=col_limit)
    elif method == 'stream':
        csv_file = reader(StringIO(file_path_or_stream.decode('utf-8')), delimiter=',')
        return get_csv_data(csv_file, row_limit=row_limit, col_limit=col_limit)
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
