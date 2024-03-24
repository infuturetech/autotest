# -*- coding: utf-8 -*-
""" 日志处理

    log_config: 返回tuple(日志句柄, 日志文件路径)

    AioLog: 实例化得到日志句柄，异步日志，可设置落盘条数
        - csv 可写文件
        - flush 立即刷盘

"""

import os
import csv
import time
import logging
from logging.handlers import RotatingFileHandler as LogHandler

import aiofiles


__all__ = ['log_config', 'AioLog', 'logging']


def log_config(f_level=logging.INFO, c_level=logging.CRITICAL, out_path='', filename='info', fix=False):
    logfile = os.path.join(out_path, filename) + '-' + time.strftime('%Y_%m%d_%H%M%S', time.localtime()) + '.txt' \
        if not fix else os.path.join(out_path, filename) + '.txt'

    # if not os.path.exists(logfile):
    #     os.mkdir(logfile)
    # print(os.getcwd())
    # print(logfile)
    logger = logging.getLogger(logfile)
    """
    1、依据logging包官方的注释，日志记录会向上传播到他的父节点也就是root logger
    2、当root logger 同时也被添加了屏幕输出handler的情况，日志就会输出第二次
    3、 root logger 若被多次添加屏幕输出handler，同一日志就会多次输出。
    pytest使用的为root logger，且添加了输出handler
    """
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    # if f_level is None:
    #     if c_level is None:
    #         logger.setLevel(logging.INFO)
    #     else:
    #         logger.setLevel(c_level)
    # else:
    #     logger.setLevel(f_level)

    formatter = logging.Formatter(
        '[%(levelname)s][%(process)d][%(thread)d]--%(asctime)s--[%(filename)s %(funcName)s %(lineno)d]: %(message)s')

    if c_level is not None:
        ch = logging.StreamHandler()
        ch.setLevel(c_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if f_level is not None:
        fh = LogHandler(logfile, maxBytes=100 * 1024 * 1024, backupCount=100)
        fh.setLevel(f_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger, logfile


class AioLog:
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __init__(self, out_path='', level=1, flush_lines=1000):
        self.out_path = out_path
        self.level = level
        self.log_file_prefix = time.strftime('%Y%m%d%H%M%S')
        self.buffer = {'debug': [], 'info': [], 'warning': [], 'error': [], 'critical': []}
        self.flush_lines = flush_lines
        self.flush_force = False
        self.log_file = {}
        for key in ['debug', 'info', 'warning', 'error', 'critical']:
            self.log_file[key] = os.path.join(out_path, f'{self.log_file_prefix}_{key}.txt')

    async def debug(self, msg=None):
        if AioLog.DEBUG >= self.level:
            if msg != '^$':
                self.buffer['debug'].append(f'[DEBUG]{time.strftime("%Y-%m-%d %H:%M:%S")} {str(msg)}\n')
            if len(self.buffer['debug']) > self.flush_lines or self.flush_force:
                tmp = self.buffer['debug'][:]
                self.buffer['debug'] = []
                if tmp:
                    async with aiofiles.open(self.log_file['debug'], 'a', encoding='utf-8') as f:
                        await f.write(''.join(tmp))

    async def info(self, msg=None):
        if AioLog.INFO >= self.level:
            if msg != '^$':
                self.buffer['info'].append(f'[INFO]{time.strftime("%Y-%m-%d %H:%M:%S")} {str(msg)}\n')
            if len(self.buffer['info']) > self.flush_lines or self.flush_force:
                tmp = self.buffer['info'][:]
                self.buffer['info'] = []
                if tmp:
                    async with aiofiles.open(self.log_file['info'], 'a', encoding='utf-8') as f:
                        await f.write(''.join(tmp))

    async def warning(self, msg=None):
        if AioLog.WARNING >= self.level:
            if msg != '^$':
                self.buffer['warning'].append(f'[WARNING]{time.strftime("%Y-%m-%d %H:%M:%S")} {str(msg)}\n')
            if len(self.buffer['warning']) > self.flush_lines or self.flush_force:
                tmp = self.buffer['warning'][:]
                self.buffer['warning'] = []
                if tmp:
                    async with aiofiles.open(self.log_file['warning'], 'a', encoding='utf-8') as f:
                        await f.write(''.join(tmp))

    async def error(self, msg=None):
        if AioLog.ERROR >= self.level:
            if msg != '^$':
                self.buffer['error'].append(f'[ERROR]{time.strftime("%Y-%m-%d %H:%M:%S")} {str(msg)}\n')
            if len(self.buffer['error']) > self.flush_lines or self.flush_force:
                tmp = self.buffer['error'][:]
                self.buffer['error'] = []
                if tmp:
                    async with aiofiles.open(self.log_file['error'], 'a', encoding='utf-8') as f:
                        await f.write(''.join(tmp))

    async def critical(self, msg=None):
        if AioLog.CRITICAL >= self.level:
            if msg != '^$':
                self.buffer['critical'].append(f'[CRITICAL]{time.strftime("%Y-%m-%d %H:%M:%S")} {str(msg)}\n')
            if len(self.buffer['critical']) > self.flush_lines or self.flush_force:
                tmp = self.buffer['critical'][:]
                self.buffer['critical'] = []
                if tmp:
                    async with aiofiles.open(self.log_file['critical'], 'a', encoding='utf-8') as f:
                        await f.write(''.join(tmp))

    async def txt(self, msg, file_path):
        if file_path and file_path not in self.buffer:
            self.buffer[file_path] = []
        if msg != '^$':
            self.buffer[file_path].append(msg + '\n')
        if file_path is None:
            file_paths = [elem for elem in self.buffer.keys() if elem not in
                          ['debug', 'info', 'warning', 'error', 'critical'] and 'csv' not in elem]
        else:
            file_paths = [file_path]
        for file_path in file_paths:
            if len(self.buffer[file_path]) >= self.flush_lines or self.flush_force:
                tmp = self.buffer[file_path][:]
                self.buffer[file_path] = []
                if tmp:
                    async with aiofiles.open(file_path, 'a', encoding='utf-8') as f:
                        await f.write(''.join(tmp))

    def csv(self, msg, file_path):
        if file_path and file_path not in self.buffer:
            self.buffer[file_path] = []
        if msg != '^$':
            self.buffer[file_path].append(msg)
        if file_path is None:
            file_paths = [elem for elem in self.buffer.keys() if elem not in
                          ['debug', 'info', 'warning', 'error', 'critical'] and 'csv' in elem]
        else:
            file_paths = [file_path]
        for file_path in file_paths:
            if len(self.buffer[file_path]) >= self.flush_lines or self.flush_force:
                tmp = self.buffer[file_path][:]
                self.buffer[file_path] = []
                with open(file_path, 'a', newline="", encoding="utf-8-sig") as fw:
                    fw_csv = csv.writer(fw)
                    fw_csv.writerows(tmp)

    async def flush(self):
        self.flush_force = True
        await self.debug('^$')
        await self.info('^$')
        await self.warning('^$')
        await self.error('^$')
        await self.critical('^$')
        await self.txt('^$', None)
        self.csv('^$', None)
        self.flush_force = False
