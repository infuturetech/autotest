# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import check_service_is_running, ctrl_service
from contants.global_vars import *

log = logging.getLogger(__name__)

@pytest.mark.p0
def test_check_ctrl_cms(host):
    """
    检查cms服务启动停止
    Args:
        host (_type_): _description_
    """
    log.info("测试点：检查cms服务启动停止")
    ctrl_service(host, CMS, "stop")
    time.sleep(5)
    ctrl_service(host, CMS, "start")
    time.sleep(8)    
    assert check_service_is_running(host, CMS)


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])