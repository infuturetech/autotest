# -*- coding: utf-8 -*-
""" http请求，封装requests和aiohttp

    Api: 通过接口参数实例化请求对象
        实例api = Api(*args, **const.kwargs)方法
            - request 只完成请求
            - get_response  完成请求+处理返回结果，返回dict

    req: 异步http请求，返回tuple(状态码，响应body，响应时长)

    s: requests的Session，可直接执行http的相关请求

"""
import os
import sys
import re
import ssl
import time
import copy
import traceback
import threading
from json import dumps, loads
from typing import Tuple

import aiohttp
from requests import adapters, Session
import urllib3

from contants.global_vars import SSH_USER, SSH_PASSWORD
from common_interface.log import AioLog, logging
from common_interface.interf_const import UrlPrefix

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__all__ = [
    'Api', 'req', 's', 'filter_long_value'
]

ca_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ca.pem')
a = adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
s = Session()
s.mount('http://', a)
s.verify = os.path.join(ca_file)

ssl_context = ssl.create_default_context(cafile=ca_file)
time_out = aiohttp.ClientTimeout(total=60)


class Api:

    def __init__(self,
                 host: str,
                 uri: str,
                 method: str,
                 body: dict = None,
                 log: logging = None,
                 log_msg_flag: bool = False,
                 timeout: int = 120,
                 protocol: str = 'http',
                 headers: dict = None,
                 params: dict = None,
                 verify: bool = None,
                 files: list = None,
                 data: dict = None):
        self.host = host
        self.uri = uri
        self.method = method
        self.body = {} if body is None else body
        self.data = {} if data is None else data
        self.params = {} if params is None else params
        self.timeout = timeout
        self.protocol = protocol

        if self.host.split(':')[-1] in [
                '30443', '30063'
        ]:  # openapi:30443, elasticsearch: 30063
            self.protocol = 'https'
        self.headers = {} if headers is None else headers
        s.verify = s.verify if verify is None else verify
        self.files = files
        self.url = None
        self.response = None
        self.response_time = None
        self.log = log
        self.status_code = None
        if self.log is None:
            self.log_flag = False
        else:
            self.log_flag = True
        self.log_msg_flag = log_msg_flag
        self.log_msg = []
        self.__max_retries = 3

    def request(self):
        token = os.environ.get("ats_headers")
        if token:
            s.headers.update(loads(token))

        t_start = time.time()
        try:
            if not isinstance(self.body, dict):
                self.url = self.protocol + '://' + self.host + self.uri.replace(
                    '{}', str(self.body))
            elif self.body == {}:
                self.url = self.protocol + '://' + self.host + self.uri
            else:
                uri_keys = re.findall(r'{(.*?)\}', self.uri)
                for key in uri_keys:
                    if key not in self.body and '[' not in key and '.' not in key and key not in UrlPrefix:
                        self.uri = self.uri.replace('{' + key + '}', '')
                if 'http' in self.host:
                    self.url = self.host + self.uri.format(
                        **self.body, **UrlPrefix)
                else:
                    self.url = self.protocol + '://' + self.host + self.uri.format(
                        **self.body, **UrlPrefix)
            if self.method == 'GET' or self.method == 'DELETE':

                self.response = s.request(self.method,
                                          self.url,
                                          params=self.body,
                                          timeout=self.timeout,
                                          headers=self.headers,
                                          data=self.data,
                                          verify=False
                                          )
            else:
                self.response = s.request(self.method,
                                          self.url,
                                          params=self.params,
                                          json=self.body,
                                          files=self.files,
                                          timeout=self.timeout,
                                          headers=self.headers,
                                          data=self.data,
                                          verify=False
                                          )
        except Exception as e:
            self.log_msg.append('-' * 120 + '\n' + time.ctime() + '\n' +
                                str(traceback.format_exc()) + '\n')
            if self.log_flag:
                self.log.error(
                    '\n' + str(self.method) + ' ' + str(self.url) + '\n' +
                    dumps(filter_long_value(copy.deepcopy(self.body))) + '\n' +
                    str(e) + '\n' + traceback.format_exc() + '\n' + '-' * 120)
        finally:
            try:
                self.status_code = self.response.status_code
            except Exception as e:
                if self.log_flag:
                    self.log.error(e)
            self.response_time = time.time() - t_start
            line_break = '\n{}\n'.format('*' * 90)
            line_break_underline = '\n\n'

            base_info = '{}Request: {}, {} {}'.format(line_break,
                                                      str(self.method),
                                                      str(self.url),
                                                      line_break_underline)
            request_info = '{}Body: {}{}'.format(
                base_info, dumps(filter_long_value(copy.deepcopy(self.body))),
                line_break_underline)
            if self.response is not None:
                request_info = '{}Headers: {}{}'.format(
                    request_info, self.response.request.headers,
                    line_break_underline)

            self.log_msg.insert(0,
                                '-' * 120 + '\n' + time.ctime() + request_info)
            if self.response is not None:
                try:
                    r = self.response.content
                    if isinstance(r, bytes):
                        response_info = str(r)
                    else:
                        response_info = dumps(
                            filter_long_value(
                                copy.deepcopy(self.response.json())))
                except Exception as e:
                    if self.log_flag:
                        self.log.warning(e.with_traceback)
                    response_info = str(self.response.content)
                response_info = 'Response: ' + str(self.response.status_code) + '  ' + \
                                str(int(self.response_time * 1000)) + \
                                'ms  \n' + response_info + '\n' + '-' * 90
                self.log_msg.append(response_info)
                if self.log_flag:
                    if self.response.status_code == 200:
                        self.log.debug(request_info + response_info)
                    else:
                        self.log.error(request_info + response_info)

    def get_response(self, flag=None) -> dict or None:
        retries = 0
        while True:
            retries += 1
            self.request()
            if retries > self.__max_retries:
                self.log.error("request reach max retry times")
                break
            if self.should_retry(self.response):
                self.log.info("request should retry")
                continue
            break
        try:
            r = self.response.json()
            if self.log_msg_flag:
                r['log_msg'] = ''.join(self.log_msg)
            self.log.info(f"response> {r}")    
            return r
        except Exception as e:
            r = self.response.content
            if isinstance(r, bytes):
                return r
            else:
                if self.log_msg_flag:
                    return {
                        'log_msg': ''.join(self.log_msg),
                        'error': 'not_json' + str(e)
                    }
                else:
                    return None
        finally:
            if self.response:
                self.response.close()

    def get_response_with_elapse(self) -> dict or None:
        retries = 0
        while True:
            retries += 1
            self.request()
            if retries > self.__max_retries:
                break
            if self.should_retry(self.response):
                continue
            break
        try:
            r = self.response.json()
            if self.log_msg_flag:
                r['log_msg'] = ''.join(self.log_msg)
            return r, self.response.elapsed.total_seconds()
        except Exception as e:
            if self.log_msg_flag:
                return {
                    'log_msg': ''.join(self.log_msg),
                    'error': 'not_json' + str(e)
                }, -1
            else:
                return None, -1
        finally:
            self.response.close()

    # def update_token(self):
    #     """更新JWT token，当前是请求sign token接口会把token保存到环境变量中
    #     """
    #     access_key, secret_key = self.get_access_key_and_secret_key(self.host)
    #     self._update_token(self.host, self.protocol, self.log,
    #                        self.log_msg_flag, access_key, secret_key)

    # @staticmethod
    # def _update_token(host, protocol, log, log_msg_flag, access_key,
    #                   secret_key):
    #     from interface.interf_const import UserManager
    #     api = Api(host=host,
    #               log=log,
    #               protocol=protocol,
    #               body={
    #                   'access_key': access_key,
    #                   'secret_key': secret_key
    #               },
    #               log_msg_flag=log_msg_flag,
    #               **UserManager.SignToken)
    #     r = api.get_response()
    #     log.info("viper sign new token: {}".format(r["token"]))
    #     os.environ["vats_headers"] = dumps(
    #         {'Authorization': 'Bearer {}'.format(r["token"])})

    def should_retry(self, resp) -> bool:
        """请求是否需要重试，如token过期等

        Args:
            resp (Response): 单次请求的Response对象

        Returns:
            bool: True需要重试；False不需要
        """
        if resp is not None and resp.status_code == 401:
            r = resp.json()
            if ("code" in r and r["code"] == 16 and "error" in r and r["error"]
                    == "jwt token is expired or wrong jwt token"):
                # self.update_token()
                return True
        if resp is not None and resp.status_code == 502:
            # An invalid response was received from the upstream server
            # 一般发生在网关和后端服务网络不稳定时
            time.sleep(1)
            return True               

        return False


async def _req(method: str,
               url: str,
               json: dict = None,
               params: dict = None,
               data: dict = None,
               headers: dict = s.headers,
               session: aiohttp.ClientSession = None,
               log: AioLog = None) -> tuple:
    """
        异步http请求
    :param method: 请求方法get/post/delete/head/update/put, 不区分大小写
    :param url: 请求地址http://host/uri或者https://host/uri
    :param json: 请求body是json类型
    :param params: 查询参数，url上的?k1=v1&k2=v2...
    :param data: 表单数据
    :param headers: 请求头部
    :param session: 会话
    :param log: 日志句柄
    :return: 状态码，响应体，响应时长
    """
    t, resp, r, resp_b = time.time(), None, None, None
    try:
        if 1 == 1:
            async with session.request(method,
                                       url,
                                       json=json,
                                       data=data,
                                       params=params,
                                       headers=headers,
                                       ssl=ssl_context,
                                       timeout=time_out) as resp:
                try:
                    resp_b = await resp.json()
                except Exception as e:
                    if log:
                        await log.warning(str(e))
                    resp_b = await resp.text()

            r = resp.status, time.time() - t, resp_b
            if log:
                if r[0] == 200:
                    await log.debug(f'{"-"*120}\nRequest: {method} {url} \n'
                                    f'Response: {r[0]} {r[1]}\n'
                                    f'{filter_long_value(copy.deepcopy(r[2]))}'
                                    )
                else:
                    await log.error(
                        f'{"-"*120}\nRequest: {method} {url} \n'
                        f'{filter_long_value(copy.deepcopy(json))}\nResponse: {r[0]} {r[1]}\n'
                        f'{filter_long_value(copy.deepcopy(r[2]))}')
    except Exception as e:
        r = resp.status if resp else None, time.time() - t, str(
            e) + '\n' + traceback.format_exc()
        if log:
            await log.critical(
                f'{"-"*120}\nRequest: {method} {url} \n'
                f'{filter_long_value(copy.deepcopy(json))}\nResponse: {r[0]} {r[1]}\n{r[2]}'
            )
    return r


async def req(host: str,
              method: str,
              uri: str,
              json: dict = None,
              params: dict = None,
              data: dict = None,
              headers: dict = s.headers,
              protocol: str = 'http',
              session: aiohttp.ClientSession = None,
              log: AioLog = None) -> tuple:
    """
        异步http请求，请求包裹ClientSession
    :param host: ip:port
    :param method: 请求方法get/post/delete/head/update/put, 不区分大小写
    :param uri: 资源地址
    :param json: 请求body是json类型
    :param params: 查询参数，url上的?k1=v1&k2=v2...
    :param data: 表单数据
    :param headers: 请求头部
    :param protocol: http/https
    :param session: 支持外部传入会话复用
    :param log: 日志句柄
    :return: 状态码，响应体，响应时长
    """
    from common_interface.func import Func
    status_code, elapse, rsp_text = None, None, None
    if '443' in host:
        protocol = 'https'
    url = f'{protocol}://{host}{uri}'
    if json:
        url = url.format(**json)
    if params:
        url = url.format(**params)
    try:

        for _ in range(0, 5):
            token = os.environ.get("vats_headers")
            if token:
                if not headers:
                    headers = s.headers
                headers.update(loads(token))            
            if session:
                status_code, elapse, rsp_text = await _req(
                    method, url, json, params, data, headers, session, log)
            else:
                async with aiohttp.ClientSession() as _session:
                    status_code, elapse, rsp_text = await _req(
                        method, url, json, params, data, headers, _session, log)
            if status_code == 401 and "jwt token is expired or wrong jwt token" in str(
                    rsp_text):
                access_key, secret_key = Api.get_access_key_and_secret_key(
                    host)
                Api._update_token(host, protocol, Func.log, None, access_key,
                                  secret_key)
                continue
            if status_code == 500 or status_code == 502:
                continue
            else:
                break
        return status_code, elapse, rsp_text
    except Exception as e:
        if log:
            await log.critical(
                f'{"-" * 120}\n{"*" * 80}\nRequest: {method} {url} \n{"*" * 80}\n'
                + str(e) + '\n' + traceback.format_exc())
        return None, None, None


def filter_long_value(obj, length=1000):
    if isinstance(obj, dict):
        for key in obj:
            _filter_long_value(obj, key, length)
    elif isinstance(obj, list):
        for index, _ in enumerate(obj):
            _filter_long_value(obj, index, length)
    return obj


def _filter_long_value(obj, position, length):
    if isinstance(obj[position], str) and len(obj[position]) >= length:
        obj[position] = "..."
    elif isinstance(obj[position], dict) or isinstance(obj[position], list):
        filter_long_value(obj[position], length)