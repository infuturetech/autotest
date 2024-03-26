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
def test_upload_not_exsit_file_path(host):
    """
    使用错误的算法uri进行上传
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 使用错误的算法uri进行上传")

    # log.info("上传算法包到仓库")
    # local_path = upload_app_file_to_server(host)
    rr = OpenApi.upload_app_packet(host, "/home/nvidia/qixin.tar.gz", algo_type=1, algo_name="人脸检测demo", algo_version="v1.0", describe="测试")
    log.info(f"算法上传rsp: {rr}")  

    assert "path not exist" == str(rr['result']["message"])


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])