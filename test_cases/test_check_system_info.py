# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import upload_app_file_to_server
from aws.tools import region_id, find_items_in_dict
from contants.global_vars import *

log = logging.getLogger(__name__)

@pytest.mark.p0
def test_check_system_info(host):
    """
    查询获取服务组件日志信息
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 查询获取服务组件日志信息")

    r = OpenApi.get_system_info(host)
    assert len(r["data"]["service"]) > 0
    

if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])