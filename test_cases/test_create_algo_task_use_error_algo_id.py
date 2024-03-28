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
def test_create_algo_task_use_error_algo_id(host):
    """
    使用不存在的算法id下发推理任务
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 使用不存在的算法id下发推理任务")
    camera_data = OpenApi.add_camera_data(host, camera_name="test_1k", region_id=region_id(), address=rtsp_1k, factory="mock", protocol="rtsp")
    log.info(f"创建点位返回结果: {camera_data}")
    _datas = find_items_in_dict(camera_data, "camera_id")
    camera_id = _datas.get("camera_id", None)
    log.info(f"相机点位id: {camera_id}")

    decoder_cfg =  {
        "strategy": "KEY",
        "step": 2
    }
  
    rr3 = OpenApi.create_algo_task(host, "error", camera_id, decode_config=decoder_cfg)
    # stream_id2 = rr3["data"]["stream_id"]
    # log.info(f"stream_id2: {stream_id2}")    
    time.sleep(2)

    OpenApi.delete_camera(host, camera_id)

    # OpenApi.delete_camera(host, camera_id2)     
    
    assert rr3["result"]["code"] != 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])