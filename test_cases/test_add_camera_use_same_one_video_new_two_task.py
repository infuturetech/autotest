# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import check_service_is_running, ctrl_service
from aws.tools import region_id, find_items_in_dict
from contants.global_vars import *

log = logging.getLogger(__name__)

@pytest.mark.p2
def test_add_camera_use_same_one_video_new_two_task(host):
    """
    使用同一条rtsp流同时创建两个相机点位可以成功1个
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 使用同一条rtsp流同时创建两个相机点位可以成功1个")
    camera_data = OpenApi.add_camera_data(host, camera_name="test_1k", region_id=region_id(), address=rtsp_1k, factory="mock", protocol="rtsp")
    log.info(f"创建点位1返回结果: {camera_data}")
    _datas = find_items_in_dict(camera_data, "camera_id")
    camera_id = _datas.get("camera_id", None)
    log.info(f"相机1点位id: {camera_id}")

    time.sleep(2)
    camera_data2 = OpenApi.add_camera_data(host, camera_name="test_2k", region_id=region_id(), address=rtsp_1k, factory="mock", protocol="rtsp")
    log.info(f"创建点位2返回结果: {camera_data2}")
    _datas2 = find_items_in_dict(camera_data2, "camera_id")
    camera_id2 = _datas2.get("camera_id", None)
    log.info(f"相机2点位id: {camera_id2}")    

    OpenApi.delete_camera(host, camera_id)

    OpenApi.delete_camera(host, camera_id2)

    assert camera_id


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])