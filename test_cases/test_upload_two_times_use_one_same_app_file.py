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
def test_upload_two_times_use_one_same_app_file(host):
    """
    使用同一算法包进行两次上传
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 使用同一算法包进行两次上传")

    log.info("上传算法包到仓库")
    local_path = upload_app_file_to_server(host)
    rr = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo", algo_version="v1.0", describe="测试")
    algo_id = rr["data"].get("algo_id", None)
    log.info(f"算法包id: {algo_id}")

    rr2 = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo", algo_version="v1.0", describe="测试")
    log.info(f"第二次上传结果: {rr2}")    

    OpenApi.delete_app_packet(host, algo_id)

    assert rr2["result"]["code"] != 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])