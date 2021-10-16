import re


# 文本分隔符号替换预处理
def replace_character(text):
    return re.sub(r'[，,、]', ',', re.sub(r'!|！|；|。|\.|\r\n|\r|\n', ';', text))


# 列表递归
def handle_deep_texts_list(lists):
    child = lists[0]
    if isinstance(child, list):
        for each_list in lists:
            handle_deep_texts_list(each_list)
    else:
        for (index, val) in enumerate(lists):
            lists[index] = replace_character(val)


# 过滤空格
def filter_space(s):
    return s and s.strip()


# 过滤列表中的空字符
def filter_empty_text(li, method='empty'):
    # 只过滤空字符和None
    if method == 'empty':
        return list(filter(None, li))
    # 过滤只含有空格的字符，如果字符中不仅含有空格，还有其他能显示的字符则不过滤，如' space  '
    elif method == "space":
        return list(filter(filter_space, li))


# 文本分行
def texts_division_to_rows(text, method='character', character=';'):
    rows = []
    if method == "enter":
        rows = text.splitlines()
    elif method == "character":
        rows = text.split(character)
    rows = filter_empty_text(rows, method='empty')
    return rows


def rows_to_table_data(rows: list, character=','):
    table_data = []
    for row in rows:
        row_data = row.split(character)
        table_data.append(filter_empty_text(row_data, method='empty'))
    return table_data


def rows_to_single_col_table_data(rows: list):
    return [[row] for row in rows]


# 完整文本数据转化为行数据预处理流程
def texts_to_rows_integral_process(text):
    return texts_division_to_rows(replace_character(text))


def texts_to_table_data_integral_process(text):
    return rows_to_table_data(texts_division_to_rows(replace_character(text)))


def texts_to_single_col_table_data_integral_process(text):
    return rows_to_single_col_table_data(texts_division_to_rows(replace_character(text)))


# 当文件比较大的时候使用这个方法读取文件，设定开始和结束的位置一行一行读，减少内存消耗，但是这种方法会慢一点
def read_large_text_file(path, start=1, end=-1):
    if end != -1 and start > end:
        return []
    now_line = 0
    done = 0
    lines = []
    with open(path, mode='r', encoding='utf8') as f:
        while not done:
            line = f.readline()
            now_line += 1
            if line == '':
                done = 1
            else:
                if end == -1 and start <= now_line:
                    lines.append(line)
                elif end != -1 and start <= now_line <= end:
                    lines.append(line)
    return lines
