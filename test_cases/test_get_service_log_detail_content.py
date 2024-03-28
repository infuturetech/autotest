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
def test_get_service_log_detail_content(host):
    """
    正确设置组件和行数查询具体的日志内容
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 正确设置组件和行数查询具体的日志内容")

    r = OpenApi.get_system_info(host)

    service = r["data"]["service"][0]
    name = service["name"]
    paths = service["path"]

    logs = OpenApi.get_service_log_detail(host, name, 5) 
    assert len(logs["data"]["line"]) > 0
    

if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])