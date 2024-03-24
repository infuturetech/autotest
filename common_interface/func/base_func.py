# -*- coding: utf-8 -*-
""" 接口http请求的基础封装

    get_item_by_key: 获取嵌套字典中任一键的值，多个值返回list

    Func: Api类的封装，可新增全局配置、日志等

    Default: 常用的字典对象默认值

    模块类，静态方法即接口的http封装

"""

import functools
import inspect
import json
import os
import threading
import time
import traceback

import yaml
from jsonpath_ng.ext import parse
# from viper_common.common.ssh.ssh import ssh_run_cmd_plus

# import viper_interface.interf_const as const
# from viper_common.common.ssh import Client
# from viper_common.constants.service.check_test_service import CheckService
from common_interface.api import Api as WrapperApi
# from viper_interface.api import token_handler
# from viper_interface.const import set_viper_version
from common_interface.log import log_config, logging


LOG_LEVEL = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10}
log = logging.getLogger(__name__)


class MyThread(threading.Thread):
    def run(self):
        self.result = False
        self.result = self._target(*self._args, **self._kwargs)


def timeout(duration):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            t = MyThread(target=f, args=args, kwargs=kwargs)
            t.daemon = True
            t.start()
            while True:
                if time.time() - start_time > duration:
                    return f'case执行时间超时，设定超时时间{duration}s'
                time.sleep(1)
                if not t.is_alive():
                    return t.result

        return wrapper

    return decorator


# def token(func):
#     @functools.wraps(func)
#     def wrap(config, log=None):

#         # http 和 https 协议处理
#         if 'host' in config and config['host'].split(':')[-1] == '30443':
#             Func.protocol = 'https'
#         else:
#             Func.protocol = 'http'

#         # token 处理
#         if 'host' in config and '30443' in config['host']:
#             token_handler(config, log)

#         # 参数替换
#         params = {}
#         for key in list(inspect.signature(func).parameters.keys()):
#             if key in config:
#                 params[key] = config[key]
#         return func(**params)
#     return wrap




def get_item_by_key(obj, key, result=None):
    if isinstance(obj, dict):
        for k in obj:
            if key == k:
                if isinstance(result, list):
                    if isinstance(obj[k], list):
                        result.extend(obj[k])
                    else:
                        result.append(obj[k])
                elif result is None:
                    result = obj[k]
                else:
                    tmp = [result]
                    result = tmp
                    result.append(obj[k])
            else:
                if isinstance(obj[k], dict) or isinstance(obj[k], list):
                    result = get_item_by_key(obj[k], key, result)
    elif isinstance(obj, list):
        for i in obj:
            if isinstance(i, dict) or isinstance(i, list):
                result = get_item_by_key(i, key, result)
    return result[0] if isinstance(result, list) and len(result) == 1 else result


def json_search(json_path, dict_data):
    """
        在dict_data中按json_path提取数据
    :param json_path: json_path的字符串表达式
    :param dict_data: 字典
    :return:
    """
    if "$" not in json_path:
        json_path = "$.." + json_path
    json_path_expr = parse(json_path)
    return [match.value for match in json_path_expr.find(dict_data)] or [
        None
    ]  # 未匹配到时返回None的列表, 避免index error


def update_value_by_path(json: dict, path: str, value) -> dict:
    """set json/dict object value by path and return updated object

    Args:
        json (dict): json or dict object
        path (str): path expression
        value (Any): target value

    Returns:
        dict: updated dict object
    """
    if "$" not in path:
        path = "$.." + path
    jsonpath_expr = parse(path)
    return jsonpath_expr.update_or_create(json, value)


class Func:
    log = log_config(c_level=logging.DEBUG, f_level=None)[0]
    log_msg_flag = False
    protocol = 'http'

    @classmethod
    def init_log(cls, c_level=logging.INFO, f_level=logging.INFO, log_path=''):
        cls.log.handlers.clear()
        cls.log = log_config(c_level=c_level, f_level=f_level, out_path=log_path)[0]
        return cls.log

    @classmethod
    def api(cls, *args, **kwargs):
        protocol = cls.protocol
        _api = WrapperApi(
            *args,
            log=cls.log,
            log_msg_flag=cls.log_msg_flag,
            protocol=protocol,
            **kwargs,
        )
        return _api


def get_config_with_sep_env():
    config = os.environ.get("config")
    if config:
        config = json.loads(config)
    else:
        config = read_from_local_config()
    return config


def read_from_local_config():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    dir_path = dir_path.split('interface')[0] + "local_config.json"
    with open(dir_path, 'r') as f:
        temp = json.loads(f.read())
        return temp

