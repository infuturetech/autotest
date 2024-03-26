# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import check_service_is_running, ctrl_service
from aws.tools import region_id, find_items_in_dict
from contants.global_vars import *

log = logging.getLogger(__name__)

@pytest.mark.p1
def test_delete_one_not_create_algo_task_camera(host):
    """
    验证删除一条已存在但未下发推理任务的相机点位
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 验证删除一条已存在但未下发推理任务的相机点位")
    camera_data = OpenApi.add_camera_data(host, camera_name="test_1k", region_id=region_id(), address=rtsp_1k, factory="mock", protocol="rtsp")
    log.info(f"创建点位返回结果: {camera_data}")
    _datas = find_items_in_dict(camera_data, "camera_id")
    camera_id = _datas.get("camera_id", None)
    log.info(f"相机点位id: {camera_id}")

    ret = OpenApi.delete_camera(host, camera_id)

    assert ret["result"]["code"] == 0


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])