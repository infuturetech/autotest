# -*- coding: utf-8 -*-

import pytest
import logging
import time

from common_interface.func.api_func import OpenApi
from aws.common import upload_app_file_to_server
from aws.tools import region_id, find_items_in_dict
from contants.global_vars import *
from aws.time_number.time import get_remote_host_utc_time

log = logging.getLogger(__name__)

@pytest.mark.p0
def test_delete_algo_results_use_right_time_range(host):
    """
    删除指定算法某个时间段的推理结果
    Args:
        host (_type_): _description_
    """
    log.info("测试点: 删除指定算法某个时间段的推理结果")
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
    decoder_cfg =  {
        "strategy": "KEY",
        "step": 2
    }

    rr2 = OpenApi.create_algo_task(host, algo_id, camera_id, decode_config=decoder_cfg)
    stream_id = rr2["data"]["stream_id"]
    log.info(f"stream_id: {stream_id}")
    
    start_time = get_remote_host_utc_time(host, is_utc=False)
    log.info(f"查询开始时间点: {start_time}")

    time.sleep(30)

    end_time = get_remote_host_utc_time(host, is_utc=False)
    log.info(f"查询开始时间点: {end_time}")

    results = OpenApi.search_algo_task_result_time_range(host, stream_id, algo_id, start_time, end_time)

    OpenApi.delete_algo_task_result_time_range(host, algo_id, start_time, end_time, stream_id)

    results2 = OpenApi.search_algo_task_result_time_range(host, stream_id, algo_id, start_time, end_time)

    OpenApi.delete_algo_task(host, algo_id, stream_id)

    time.sleep(5)

    tasks = OpenApi.get_algo_task_list(host)

    ret = OpenApi.delete_camera(host, camera_id)

    OpenApi.delete_app_packet(host, algo_id)
    
    assert len(results["data"]) != len(results2["data"])


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])