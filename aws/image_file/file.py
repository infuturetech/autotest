import os
import time
import hashlib
import random
import re
import base64
import copy
import json
import sys

from jsonpath_rw import parse


def get_file_create_time(path):
    timestamp = os.path.getctime(path)
    time_struct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)


def create_dir(path):
    """Creates a directory if it does not exist already.

    Args:
        path: The path of the directory to create.
    """
    full_path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(full_path):
        os.makedirs(full_path, exist_ok=True)


def get_files(case_path, pic_list):
    """
    此方法为了方便后面的test用例名获取显示
    :param case_path: 用例的绝对路径
    :param pic_list: pic list ,entrance is none
    :return: pic_list pic list
    """
    ext = ["jpg", "png", "bmp", "jpeg", "gif"]
    files = os.listdir(case_path)
    # print(len(files))
    for fi in files:
        fi_d = os.path.join(case_path, fi)
        if os.path.isdir(fi_d):
            get_files(fi_d, pic_list)
        else:
            if fi_d.split(".")[-1].lower() in ext:
                pic_list.append(os.path.join(case_path, fi_d))
    return pic_list


def find_by_json_path(json_path, raw):
    """
        在raw中按json_path提取数据
    :param json_path: json_path的字符串表达式
    :param raw: 字典
    :return:
    """
    json_path_expr = parse(json_path)
    return json_path_expr.find(raw)


def _md5(filename):
    with open(filename, "rb") as fd:
        content = fd.read()
        fd.close()
        m = hashlib.md5(content)
        file_md5 = m.hexdigest()
        return file_md5


def md5(full_file_name):
    abs_full_file_name = tlang_abs_path(full_file_name)
    return _md5(abs_full_file_name)


def md5_str(content):
    m = hashlib.md5(content)
    md5_value = m.hexdigest()
    return md5_value


def tlang_abs_path(path):
    """
    :param path: file path
    :return: abs path for input path
    """
    if os.path.isabs(path):
        return path
    else:
        return os.path.join(os.environ["HOME_PATH"], path)


def file_size(full_file_name):
    abs_full_file_name = tlang_abs_path(full_file_name)
    return os.path.getsize(abs_full_file_name)


def _all_file(full_path, _filter=""):
    file_list = os.listdir(full_path)
    if "" == _filter:
        return file_list
    return filter(lambda f: re.match(_filter, f), file_list)


def rand_file(full_path, _filter):
    full_path = tlang_abs_path(full_path)
    if not os.path.isdir(full_path):
        raise Exception("infra.rand_file: input [%s] should be a directory." % full_path)
    file_list = _all_file(full_path, _filter=_filter)
    if 0 == len(file_list):
        raise Exception("can not find identified file at directory [%s]." % full_path)
    return os.path.join(full_path, random.choice(file_list))


def get_rand_file(full_path, ffilter):
    abs_file_path = tlang_abs_path(full_path)
    return rand_file(abs_file_path, ffilter)


def file_binary(full_file_name):
    abs_full_file_name = tlang_abs_path(full_file_name)
    with open(abs_full_file_name, "rb") as f:
        return f.read()


def base64_file_binary(full_file_name):
    abs_file_path = tlang_abs_path(full_file_name)
    return base64.b64encode(file_binary(abs_file_path)).decode('utf8')


def read_file_lines(full_file_name, delimiter, contain, not_contain):
    abs_full_file_name = tlang_abs_path(full_file_name)
    result = []
    with open(abs_full_file_name, "r", encoding='utf-8') as f:
        for line in f:
            line = line.rstrip("\n")
            if "" != line.strip():
                if contain in line:
                    if "" == not_contain or ("" != not_contain and not_contain not in line):
                        result.append(line)
    if "" != delimiter:
        for i, e in enumerate(result):
            result[i] = [j.strip() for j in re.split(delimiter, e)]
    return result


def is_json(var_str):
    if isinstance(var_str, str):
        try:
            json.loads(var_str)
            return True
        except:
            return False
    else:
        return False


def serialize(value):
    if isinstance(value, dict):
        for k, v in value.items():
            value[k] = serialize(v)
    elif isinstance(value, (list, tuple)):
        if isinstance(value, tuple):
            value = list(value)
        for index, i in enumerate(value):
            value[index] = serialize(i)
    elif isinstance(value, (bool, int, float)):
        value = str(value)
    elif isinstance(value, bytes):
        value = value.decode()
    else:
        value = str(value)
    return value


def format_get(value):
    if isinstance(value, (tuple, list)):
        new_value = copy.deepcopy(value)
        fmt_content = json.dumps(serialize(new_value), ensure_ascii=False, indent=4)
    elif isinstance(value, dict):
        new_value = copy.deepcopy(value)
        fmt_content = json.dumps(serialize(new_value), ensure_ascii=False, indent=4)
    elif is_json(value):
        new_value = json.loads(value)
        fmt_content = json.dumps(new_value, ensure_ascii=False, indent=4)
    elif isinstance(value, (bool, int, float)):
        fmt_content = value
    elif isinstance(value, bytes):
        fmt_content = value.decode()
    else:
        fmt_content = str(value)
    return fmt_content


def format_print(value, dst=sys.stdout):
    dst.write(format_get(value) + "\n")


def print_to_file(content, abs_file_path=None, write_mode="a"):
    """
    :param content: value to write to
    :param abs_file_path: destination file, default is sys.stdout
    :param write_mode: write mode, default is "a"
    :return: None
    """
    if abs_file_path is None:
        format_print(content)
    else:
        write_path = os.path.split(abs_file_path)[0]
        if not os.path.exists(write_path):
            os.makedirs(write_path)
        with open(abs_file_path, write_mode) as f:
            format_print(content, dst=f)


def append_update_dict(dst_dict, src_dict):
    for k, v in src_dict.items():
        if k in dst_dict.keys():
            if not isinstance(dst_dict[k], list):
                dst_dict[k] = [dst_dict[k]]
            dst_dict[k].extend(v) if isinstance(v, list) else dst_dict[k].append(v)
        else:
            dst_dict.update({k: v})


def traverse_dict_by_filter(value, filter_list=[]):
    copy_value = copy.deepcopy(value)
    result = {}
    name_list = list(set(filter_list))
    want_filter = True if 0 < len(name_list) else False
    if isinstance(copy_value, dict):
        for k, v in copy_value.items():
            if want_filter and k in name_list:
                append_update_dict(result, {k: v})
                append_update_dict(result, traverse_dict_by_filter(v, name_list))
                continue
            if isinstance(v, dict):
                sub = traverse_dict_by_filter(v, name_list)
                append_update_dict(result, sub)
            elif isinstance(v, list):
                for i in v:
                    append_update_dict(result, traverse_dict_by_filter(i, name_list))
            else:
                append_update_dict(result, {k: v} if not want_filter or k in name_list else {})
    elif isinstance(copy_value, list):
        for i in copy_value:
            append_update_dict(result, traverse_dict_by_filter(i, name_list))
    return result


def recurve_scan_files(abs_path):
    file_list = []
    for home_path, dirs, files in os.walk(abs_path):
        file_list.extend([os.path.join(home_path, f) for f in files])
    return file_list


def print_many_to_file(*args, **kwargs):
    """
    :param args: value to write to
    :param kwargs: to_file->destination file, default is sys.stdout
    :return: None
    """
    for value in args:
        print_to_file(value, abs_file_path=kwargs.get("to_file", None), write_mode=kwargs.get("write_mode", "a"))
