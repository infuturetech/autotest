# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import upload_app_file_to_server
from aws.tools import region_id, find_items_in_dict
from contants.global_vars import *

log = logging.getLogger(__name__)

@pytest.mark.p0
def test_upload_the_right_app_path(host):
    """
    验证上传一条路径正确的算法包
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 验证上传一条路径正确的算法包")
    camera_data = OpenApi.add_camera_data(host, camera_name="test_1k", region_id=region_id(), address=rtsp_1k, factory="mock", protocol="rtsp")
    log.info(f"创建点位返回结果: {camera_data}")
    _datas = find_items_in_dict(camera_data, "camera_id")
    camera_id = _datas.get("camera_id", None)
    log.info(f"相机点位id: {camera_id}")

    log.info("上传算法包到仓库")
    local_path = upload_app_file_to_server(host)
    rr = OpenApi.upload_app_packet(host, local_path, algo_type=1, algo_name="人脸检测demo", algo_version="v1.0", describe="测试")
    algo_id = rr["data"].get("algo_id", None)
    log.info(f"算法包id: {algo_id}")

    OpenApi.delete_app_packet(host, algo_id)

    assert algo_id


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])