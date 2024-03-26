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
def test_upload_two_diff_app_files(host):
    """
    验证上传两条路径正确的算法包
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 验证上传两条路径正确的算法包")

    log.info("上传算法包到仓库")
    local_path = upload_app_file_to_server(host)
    rr = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo", algo_version="v1.0", describe="测试")
    algo_id = rr["data"].get("algo_id", None)
    log.info(f"算法包id: {algo_id}")

    rr2 = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo2", algo_version="v2.0", describe="测试")
    algo_id2 = rr2["data"].get("algo_id", None)
    log.info(f"算法包id: {algo_id2}") 

    OpenApi.delete_app_packet(host, algo_id)
    OpenApi.delete_app_packet(host, algo_id2)    

    assert algo_id and algo_id2


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])