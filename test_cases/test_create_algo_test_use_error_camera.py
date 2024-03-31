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
def test_create_algo_test_use_error_camera(host):
    """
    使用不存在的相机id下发推理任务
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 使用不存在的相机id下发推理任务") 

    log.info("上传算法包到仓库")
    local_path = upload_app_file_to_server(host)
    rr = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo", algo_version="v1.0", describe="测试")
    algo_id = rr["data"]["algo_id"]
    log.info(f"算法包id: {algo_id}")    

    decoder_cfg =  {
        "strategy": "KEY",
        "step": 2
    }

    rr2 = OpenApi.create_algo_task(host, algo_id, "camera_1711287166", decode_config=decoder_cfg)

    time.sleep(2)     

    OpenApi.delete_app_packet(host, algo_id)
    
    assert rr2["result"]["code"] != 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])