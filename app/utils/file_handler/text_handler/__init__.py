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
