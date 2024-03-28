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
def test_not_create_any_algo_task_get_task_list(host):
    """
    未下发推理任务时，查询算法实例列表
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 未下发推理任务时，查询算法实例列表")

    r = OpenApi.get_algo_task_list(host)
    
    assert len(r["data"]) == 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])