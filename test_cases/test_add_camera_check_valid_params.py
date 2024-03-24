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
def test_add_camera_check_valid_params(host):
    """
    添加相机进行参数合法性校验
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 添加相机进行参数合法性校验")
    body = {
                "camera_name": "test_face_detect",
                "region_id": str(region_id()),
                "address": rtsp_1k,
                "factory": "mock",
                "protocol": "rtsp"
            }    
    camera_data = OpenApi.add_camera_data(host, camera_name="test_1k", region_id=region_id(), address=rtsp_1k, factory="mock", protocol="rtsp", body=body)
    log.info(f"创建点位返回结果: {camera_data}")
    _datas = find_items_in_dict(camera_data, ["code", "check failed"])
    camera_id = _datas.get("camera_id", None)
    log.info(f"相机点位id: {camera_id}")

    OpenApi.delete_camera(host, "camera_1711287148")

    assert True


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])