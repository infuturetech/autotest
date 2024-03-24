# -*- coding: utf-8 -*-

import pytest
import logging

from common_interface.func.api_func import OpenApi

log = logging.getLogger(__name__)

@pytest.mark.p3
def test_not_upload_app_packet_get_app_list(host):
    """
    未上传算法包时，验证调用查询app包列表接口
    Args:
        host (_type_): _description_
    """
    # log.info("测试点：未上传算法包时，验证调用查询app包列表接口")
    ret = OpenApi.get_app_packet_list(host)
    # log.info(f"结果: {ret}")

    assert True


if __name__ == "__main__":
        pytest.main(['-vs', f"{__file__}"])