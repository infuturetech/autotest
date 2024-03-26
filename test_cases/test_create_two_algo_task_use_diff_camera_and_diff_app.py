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
def test_create_two_algo_task_use_diff_camera_and_diff_app(host):
    """
    同一相机同时使用不同的算法和不同的解码下发2次推理任务
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 同一相机使用相同的解码配置同时成功下发两路推理任务")
    camera_data = OpenApi.add_camera_data(host, camera_name="test_1k", region_id=region_id(), address=rtsp_1k, factory="mock", protocol="rtsp")
    log.info(f"创建点位返回结果: {camera_data}")
    _datas = find_items_in_dict(camera_data, "camera_id")
    camera_id = _datas.get("camera_id", None)
    log.info(f"相机点位id: {camera_id}")

    log.info("上传算法包到仓库")
    local_path = upload_app_file_to_server(host)
    rr = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo", algo_version="v1.0", describe="测试")
    algo_id = rr["data"]["algo_id"]
    log.info(f"算法包id: {algo_id}")    
    
    rr2 = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo2", algo_version="v2.0", describe="测试")
    algo_id2 = rr2["data"]["algo_id"]
    log.info(f"算法包id2: {algo_id2}")

    decoder_cfg =  {
        "strategy": "KEY",
        "step": 2
    }

    rr2 = OpenApi.create_algo_task(host, algo_id, camera_id, decode_config=decoder_cfg)
    stream_id = rr2["data"]["stream_id"]
    log.info(f"stream_id: {stream_id}")
    time.sleep(5)    

    rr3 = OpenApi.create_algo_task(host, algo_id2, camera_id, decode_config=decoder_cfg)
    stream_id2 = rr3["data"]["stream_id"]
    log.info(f"stream_id2: {stream_id2}")    
    time.sleep(10)

    ret = OpenApi.delete_camera(host, camera_id)

    OpenApi.delete_app_packet(host, algo_id)
    
    assert stream_id and stream_id2


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])