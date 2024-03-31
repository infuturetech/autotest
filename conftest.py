import logging
import json
import os
import re
import pytest
from _pytest.warning_types import PytestUnknownMarkWarning
import time

import sys

from _pytest.python import Metafunc
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.config import Config
from typing import Tuple
from typing import Optional
from typing import List
import warnings
from common_interface.func.api_func import OpenApi

log = logging.getLogger("conftest")


def get_config_with_sep_env():
    config = os.environ.get("config")
    if config:
        config = json.loads(config)
    else:
        config = read_from_local_config()
    return config


def read_from_local_config():
    _dir_path = os.path.abspath(os.path.dirname(__file__))
    dir_path =os.path.join(_dir_path, "local_config.json")
    with open(dir_path, 'r') as f:
        temp = json.loads(f.read())
        return temp

config = get_config_with_sep_env()

def pytest_addoption(parser):
    """增加pytest命令行参数

    Args:
        parser (_pytest.config.argparsing.Parser): pytest参数解析器
    """
    parser.addoption("--isSkipVersion", action="store", nargs=2, help="skip running tests matching the Version Range")


def pytest_configure(config):
    """初始化pytest配置

    Args:
        config (_pytest.config.Config): Pytest Config对象
    """
    config.addinivalue_line("markers", "isSkipVersion(version_list): mark test to skip once match the version requirement")


def pytest_runtest_logstart(nodeid: str, location: Tuple[str, Optional[int], str]):
    filename, lineno, testname = location
    try:
        classname, functionname = testname.split(".", 1)
        if "[" in functionname:
            functionname = functionname.split("[", 1)[0]
        py_module = __import__(filename[:-3].replace(os.sep, "."), fromlist=[classname])
        testclass = getattr(py_module, classname, None)
        testfunc = getattr(testclass, functionname, None)
        log.info("STARTED test: {}".format(testfunc.__doc__.strip().split("\n")[0]))
    except Exception:
        log.info("STARTED test: {}".format(nodeid))


def pytest_runtest_setup(item: pytest.Item):

    try:
        clear_env(host)
    except:
        pass
    try:
        setattr(item.obj, "start_time", time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(int(time.time() - 8*3600))))
    except Exception:
        setattr(item.obj.__func__, "start_time", time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(int(time.time() - 8*3600))))
    if config.get("case_version") is None:
        return
    case_version = float(config.get("case_version")[1:].replace("_", "."))
    # 配置参数中case_version小于测试用例标签version，则跳过
    find_version_mark = [m.name for m in item.iter_markers() if re.fullmatch(r"v\d_\d", m.name)]
    if (
        config.get("case_version") is not None
        and len(find_version_mark) > 0
        and config.get("case_version") < find_version_mark[0]
    ):
        pytest.skip("Skipped: input version[%s] < test version[%s]" % (config.get("case_version"), find_version_mark[0]))
    # case_version参数满足isSkipVersion条件判断, 跳过该用例
    patterns = [mark.args for mark in item.iter_markers(name="skipVersion")]
    if patterns:
        # merge multi markers
        pattern = []
        reasons = set()
        for item in patterns:
            if isinstance(item[0], list):
                pattern.extend(item[0])
            elif isinstance(item[0], float):
                pattern.append(item[0])
            if len(item) < 2:
                raise ValueError("请填写跳过执行的原因")
            reasons.add(item[1])
        results = []
        for item in pattern:
            if isinstance(item, tuple):
                lower = item[0]
                upper = item[1] if len(item) == 2 else float("inf")
                results.append(lower <= case_version <= upper)
            elif isinstance(item, float):
                results.append(case_version == item)
        if any(results):
            pytest.skip(
                f"跳过执行: 原因({reasons}), 当前版本<{case_version}>, 符合跳过执行的条件: {patterns}, "
                + "说明: 浮点数指定跳过的单个版本; 元组指定跳过的版本闭区间, 即满足tuple[0]<=当前版本<=tuple[1]"
            )

def pytest_sessionfinish(session, exitstatus):
    # allure报告展示环境参数
    report_dir = session.config.option.allure_report_dir
    env_details = config
    if report_dir:
        with open('{}/{}'.format(report_dir, 'environment.properties'), 'w') as allure_env:
            for k, v in config.items():
                allure_env.write('{}: {}\n'.format(k, v))


def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]):
    # 依赖修改配置相关的测试用例重新排序
    items.sort(key=lambda item: getattr(item.obj, "__vats_order__", 0))
    for item in items:
        item.add_marker(item.originalname)

        # item的name和nodeid的中文显示在控制台上
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


# 获取每个阶段(setup call teardown)测试结果
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    '''
    当setup执行失败了, setup的执行结果的failed,后面的call用例和teardown都不会执行了
    如果setup正常执行, 但是测试用例call失败了,teardown 会正常执行
    如果setup正常执行, 测试用例call正常执行, teardown失败了, 最终统计的结果： 1 passed, 1 error
    '''
    try:
        pod_labels = getattr(item.obj, "pod_labels", [])
    except Exception:
        pod_labels = getattr(item.obj.__func__, "pod_labels", [])

    out = yield # 获取setup/call/teardown的执行结果

    if pod_labels:
        try:
            if not hasattr(item.obj, "test_status"):
                setattr(item.obj, "test_status", "")
        except Exception:
            if not hasattr(item.obj.__func__, "test_status"):
                setattr(item.obj.__func__, "test_status", "")

        result = out.get_result()
        if result.outcome != "passed":
            message = "{}-failed".format(result.when)
        else:
            message = "{}-passed".format(result.when)

        try:
            msg = getattr(item.obj, "test_status")
            setattr(item.obj, "test_status", ";".join([msg, message]))
        except Exception:
            msg = getattr(item.obj.__func__, "test_status")
            setattr(item.obj.__func__, "test_status", ";".join([msg, message]))

        if result.when == "teardown":
            try:
                start_time = getattr(item.obj, "start_time")
                test_status = getattr(item.obj, "test_status")
                pod_labels = getattr(item.obj, "pod_labels", [])
            except Exception:
                start_time = getattr(item.obj.__func__, "start_time")
                test_status = getattr(item.obj.__func__, "test_status")
                pod_labels = getattr(item.obj.__func__, "pod_labels", [])


@pytest.fixture(scope="session", autouse=True)
def clear_env(host):
    log.info("清理环境")

    instances = OpenApi.get_algo_task_list(host)
    tasks = instances.get("data", [])
    if tasks:
        for task in tasks:
            algo_id = task["algo_id"]
            stream_id = task["stream_id"]            
            OpenApi.delete_algo_task(host, algo_id, stream_id)

    apps = OpenApi.get_app_packet_list(host)
    datas = apps.get("data", [])
    if datas:
        for app in datas:
            algo_id = app["algo_id"]
            OpenApi.delete_app_packet(host, algo_id)


@pytest.fixture(scope="session")
def host() -> str:
    """
    :return:
    """
    return config.get("host")


@pytest.fixture(scope="session")
def log_folder():
    """
    :return:
    """
    return config.get("log_folder", None)


@pytest.fixture(scope="session", autouse=True)
def prepare_logger_log_level():
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    logging.getLogger("aiokafka").setLevel(logging.ERROR)
    return ""
