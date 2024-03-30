# -*- coding: utf-8 -*-
""" 平台接口的uri、method常量；

    类区分模块，类变量区分接口，类变量值为uri、method字典

    示例：
        class ModuleName:
            InterfaceName = {'uri': 'xxx', 'method': 'xxx'}
            ...

"""

__all__ = [
    "API_URLS",
    "UrlPrefix"
]

UrlPrefix = {"iis_prefix": "/engine/image-ingress"}

class API_URLS:

    # 添加相机
    ADD_CAMERA = {"method": "POST", "uri": "/openapi/v1/camera/add"}

    # 上传算法包
    UPLOAD_APP_PACKET = {"method": "POST", "uri": "/openapi/v1/algo/packet/upload"}

    # 查看算法包列表
    GET_APP_PACKET_LIST = {"method": "GET", "uri": "/openapi/v1/algo/packet/list"}

    # 删除指定算法包
    DELETE_APP_PACKET = {"method": "POST", "uri": "/openapi/v1/algo/packet/delete"}

    # 创建算法推理任务
    CREATE_ALGO_TASK = {"method": "POST", "uri": "/openapi/v1/algo/ins/create"}

    # 设置算法结果回调接口
    SET_ALGO_RESULT_CALL_BACK = {"method": "POST", "uri": "/openapi/v1/managecore/notify"}

    # 查询算法推理任务列表
    GET_ALGO_TASK_LIST = {"method": "GET", "uri": "/openapi/v1/algo/ins/list"}

    # 查看组件日志路径列表
    GET_LOG_PATH_LIST =  {"method": "GET", "uri": "/openapi/v1/system/info"}

    # 查看指定组件日志文件内容
    GET_LOG_DETAIL = {"method": "POST", "uri": "/openapi/v1/system/logtail"}

    # 根据时间范围搜索推理结果
    QUERY_ALGO_RESULT_BY_TIME_RANGE = {"method": "POST", "uri": "/openapi/v1/managecore/search"}

    # 删除指定推理结果
    DELETE_ALGO_RESULT = {"method": "POST", "uri": "/openapi/v1/managecore/delete"}

    # 根据时间范围删除推理结果
    DELETE_ALGO_RESULT_BY_TIME_RANGE = {"method": "POST", "uri": "/openapi/v1/managecore/batch_delete"}

    # 配置中心-查询配置
    GET_CONFIG_LIST =  {"method": "GET", "uri": "/openapi/v1/system/info"}

    # 删除算法推理任务
    DELETE_ALGO_TASK = {"method": "POST", "uri": "/openapi/v1/algo/ins/delete"}

    # 删除相机
    DELETE_CAMERA = {"method": "POST", "uri": "/openapi/v1/camera/delete"}    

    # 注册回调
    SET_CALL_BACK = {"method": "POST", "uri": "/openapi/v1/managecore/notify"}   

