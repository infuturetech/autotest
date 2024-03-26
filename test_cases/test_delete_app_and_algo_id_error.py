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
def test_delete_app_and_algo_id_error(host):
    """
    指定一条不存在的algo_id进行app包删除
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 指定一条不存在的algo_id进行app包删除")


    ret = OpenApi.delete_app_packet(host, "qixin666")
    
    assert ret["result"]["code"] == 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])