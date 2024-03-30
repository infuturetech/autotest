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
def test_delete_invalid_alg_result_id(host):
    """
    删除一条不存在的算法推理结果
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 删除一条不存在的算法推理结果")

    # log.info("上传算法包到仓库")
    # local_path = upload_app_file_to_server(host)
    rr = OpenApi.delte_algo_task_result_by_id(host, "test001")

    assert rr["result"]["code"] == 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])