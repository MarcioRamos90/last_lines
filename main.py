
import io
import os

new_lines = ["\n"]
new_lines_bytes = [n.encode("ascii") for n in new_lines]


def _get_file_size(fp):
  return os.fstat(fp.fileno()).st_size


def _is_partially_read_new_line(b):
    for n in new_lines_bytes:
        if n.find(b) >= 1:
            return True
    return False


def _get_what_to_read_next(fp, previously_read_position, chunk_size):
    seek_position = max(previously_read_position - chunk_size, 0)
    read_size = chunk_size

    while seek_position > 0:
        fp.seek(seek_position)
        if _is_partially_read_new_line(fp.read(1)):
            seek_position -= 1
            read_size += 1
        else:
            break

    read_size = min(previously_read_position - seek_position, read_size)
    return seek_position, read_size


def _get_next_chunk(fp, previously_read_position, chunk_size):
    seek_position, read_size = _get_what_to_read_next(fp, previously_read_position, chunk_size)
    fp.seek(seek_position)
    read_content = fp.read(read_size)
    read_position = seek_position
    return read_content, read_position


def _all_content(fp, read_position, chunk):
    buffer = b""
    while read_position > 0:
        read_content, read_position = _get_next_chunk(fp, read_position, chunk)
        buffer = read_content + buffer
    return buffer.decode("utf-8")


def _content_conv(c: str):
    s = []
    c = c.split(new_lines[0])
    for idx, item in enumerate(c):
        if len(item) > 0:
            if idx < len(c)-1:
                s.append(item + new_lines[0])
            else:
                s.append(item)
    s = reversed(s)
    return s
    

def last_lines(filename, chunk = io.DEFAULT_BUFFER_SIZE):
    content = None

    with open(filename, "rb") as fp:
        read_position = _get_file_size(fp)  
        all_content = _all_content(fp, read_position, chunk)
        content = _content_conv(all_content)
        
    return content


if __name__ == '__main__':
    lines = last_lines("my_file.txt")
    print(next(lines))
    print(next(lines))
    print(next(lines))

    for l in last_lines("my_file.txt"):
        print(l, end='')
