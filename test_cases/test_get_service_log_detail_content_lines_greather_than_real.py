# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import upload_app_file_to_server
from aws.tools import region_id, find_items_in_dict
from contants.global_vars import *

log = logging.getLogger(__name__)

@pytest.mark.p1
def test_get_service_log_detail_content_lines_greather_than_real(host):
    """
    查询组件日志内容设置的行数大于实际的内容数量
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 查询组件日志内容设置的行数大于实际的内容数量")

    r = OpenApi.get_system_info(host)

    service = r["data"]["service"][1]
    name = service["name"]
    paths = service["path"]

    logs = OpenApi.get_service_log_detail(host, name, 10000) 
    assert logs
    

if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])