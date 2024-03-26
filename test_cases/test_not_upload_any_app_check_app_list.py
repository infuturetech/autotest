# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import upload_app_file_to_server
from aws.tools import region_id, find_items_in_dict
from contants.global_vars import *

log = logging.getLogger(__name__)

@pytest.mark.p2
def test_not_upload_any_app_check_app_list(host):
    """
    未上传算法包时进行算法包列表查询
    Args:
        host (_type_): _description_
    """
    log.info("测试点:未上传算法包时进行算法包列表查询")
  
    apps = OpenApi.get_app_packet_list(host)

    assert len(apps["data"]) == 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])