# 盒子平台服务接口封装

import common_interface.interf_const as const

from common_interface.func.base_func import Func

log = Func.log

class OpenApi:

    @staticmethod
    def get_app_packet_list(host):
        """
        查询已上传的算法包列表
        :param host: 被测试主机
        :return: dict
            {
            "result": {
                "code": 0,
                "message": ""
            },
            "data": [
                {
                "algo_type": "Detect",
                "algo_name": "sample",
                "algo_version": "v1",
                "describe": "人脸检测",
                "instance": [],
                "algo_id": "Detect_1710563249"
                }
            ]
            }

        """
        log.info(f"invoke {const.API_URLS.GET_APP_PACKET_LIST}")
        body = {}
        api = Func.api(host, body=body, **const.API_URLS.GET_APP_PACKET_LIST)
        return api.get_response()

    
    @staticmethod
    def add_camera_data(host, camera_name, region_id, address, factory, protocol="rtsp", body=None):
        """
        添加相机
        Args:
            host (_type_): 被测试主机
            camera_name (_type_): 点位名称
            region_id (_type_): 区域id
            address (_type_): 相机流地址
            factory (_type_): 相机厂商
            protocol (str, optional): 协议. Defaults to "rtsp".
        return dict
            eg. {"result":{"code":0,"message":""},"data":{"camera_id":"camera_1710563252"}}    
        """
        if not body:
            body = {
                "name": camera_name,
                "region_id": str(region_id),
                "address": address,
                "factory": factory,
                "protocol": protocol
            }

        log.info(f"invoke {const.API_URLS.ADD_CAMERA} {body}")
        api = Func.api(host, body=body, **const.API_URLS.ADD_CAMERA)
        return api.get_response()        
    
    @staticmethod
    def upload_app_packet(host, app_packet_local_uri, algo_type, algo_name, algo_version, describe):
        """
        上传算法app包
        Args:
            host (_type_): 被测试主机
            app_packet_local_uri (_type_): 算法包本地绝对路径
            algo_type (_type_): 算法类型
            algo_name (_type_): 算法包名称
            algo_version (_type_): 算法包版本
            describe (_type_): 算法包描述
        return dict
            eg. {"result":{"code":0,"message":""},"data":{"algo_id":"Detect_1710563249"}}    
        """
        body = {
            "app_packet_local_uri": app_packet_local_uri,
            "algo_type": algo_type,
            "algo_name": algo_name,
            "algo_version": algo_version,
            "describe": describe
        }
        log.info(f"invoke {const.API_URLS.UPLOAD_APP_PACKET} {body}")        
        api = Func.api(host, body=body, **const.API_URLS.UPLOAD_APP_PACKET)
        return api.get_response()    

    @staticmethod
    def create_algo_task(host, algo_id, camera_id, decode_config):
        """
        创建算法推理任务
        Args:
            host (_type_): _description_
            algo_id (_type_): 算法id; 算法包上传时返回
            camera_id (_type_): 相机id; 创建相机时返回
            decode_config: 解码配置
                eg.  
                    {
                        "strategy": "KEY",
                        "step": 2
                    }
        return: 
            {"result":{"code":0,"message":""},"data":{"algo_id":"Detect_1710563249","stream_id":"stream_1710563252_2"}}            

        """
        body = {
            "algo_id": algo_id,
            "camera_id": camera_id,
            "screenshot": decode_config
        }
        log.info(f"invoke {const.API_URLS.CREATE_ALGO_TASK} {body}")            
        api = Func.api(host, body=body, **const.API_URLS.CREATE_ALGO_TASK)
        return api.get_response()            
    
    @staticmethod
    def set_call_back(host, stream_id, post_url):
        """
        设置推理结果回调服务接口
        Args:
            host (_type_): _description_
            stream_id (_type_): 流id; 创建算法推理任务时返回, 同一个点位同一个解码配置对应一条
            post_url (_type_): 三方接收推理接口服务接口 http://xxxxx:9988/callback
        """
        body = {
            "stream_id": stream_id,
            "post_url": post_url
        }
        log.info(f"invoke {const.API_URLS.SET_CALL_BACK} {body}")          
        api = Func.api(host, body=body, **const.API_URLS.SET_CALL_BACK)
        return api.get_response()  

    @staticmethod
    def get_algo_task_list(host):
        """
        查询算法推理任务列表
        :param host: 被测试主机
        :return: dict
            {
            "result": {
                "code": 0,
                "message": ""
            },
            "data": [
                {
                "algo_id": "xxxx",
                "stream_id": "xxxx",
                "state": "RUNNING",
                "describe": "人脸检测",
                "create_at": ""
                }
            ]
            }

        """
        body = {}
        log.info(f"invoke {const.API_URLS.GET_ALGO_TASK_LIST} {body}")          
        api = Func.api(host, body=body, **const.API_URLS.GET_ALGO_TASK_LIST)
        return api.get_response()


    @staticmethod
    def get_system_info(host):
        """
        查询系统信息
        :param host: 被测试主机
        :return: dict
            {
            "result": {
                "code": 0,
                "message": ""
            },
            "data":
                {
                    "service": [
                        {
                            "name": "AMS",
                            "path": [
                                "/home/nvidia/boxlog/ams/20240310.stdout.log"
                            ]
                        }
                        ...
                    ]
                }
            }

        """
        body = {}
        log.info(f"invoke {const.API_URLS.GET_LOG_PATH_LIST} {body}")            
        api = Func.api(host, body=body, **const.API_URLS.GET_LOG_PATH_LIST)
        return api.get_response()

    @staticmethod
    def get_service_log_detail(host, service_name, line_num):
        """
        查询指定服务日志内容
        Args:
            host (_type_): _description_
            service_name (_type_): 服务名称
            line_num (_type_): 指定日志行数
        """
        body = {
            "service_name": service_name,
            "line_num": line_num
        }
        log.info(f"invoke {const.API_URLS.GET_LOG_DETAIL} {body}")          
        api = Func.api(host, body=body, **const.API_URLS.GET_LOG_DETAIL)
        return api.get_response()    

    @staticmethod
    def search_algo_task_result_time_range(host, stream_id, algo_id, start_time=None, end_time=None):
        """
        查询时间范围内指定推理任务结果
        Args:
            host (_type_): _description_
            stream_id (_type_): 流id; 创建算法推理任务时返回, 同一个点位同一个解码配置对应一条
            algo_id (_type_): 算法id; 算法包上传时返回
            start_time: 开始时间戳
            end_time: 结束时间戳             
        """
        body = {
            "stream_id": stream_id,
            "algo_id": algo_id
        }
        if start_time:
            body["start_time"] = start_time
        if end_time:
            body["end_time"] = end_time  
        log.info(f"invoke {const.API_URLS.QUERY_ALGO_RESULT_BY_TIME_RANGE} {body}")                        
        api = Func.api(host, body=body, **const.API_URLS.QUERY_ALGO_RESULT_BY_TIME_RANGE)
        return api.get_response()            

    @staticmethod
    def delte_algo_task_result_by_id(host, algo_result_id):
        """
        根据id删除推理结果
        Args:
            host (_type_): _description_
            algo_result_id (_type_): 推理结果id, 全局唯一        
        """
        body = {
            "algo_result_id": algo_result_id
        }    
        log.info(f"invoke {const.API_URLS.DELETE_ALGO_RESULT} {body}")                  
        api = Func.api(host, body=body, **const.API_URLS.DELETE_ALGO_RESULT)
        return api.get_response()   

    @staticmethod
    def delete_algo_task_result_time_range(host, algo_id, start_time=None, end_time=None, stream_id=None):
        """
        删除时间范围内指定推理任务结果
        Args:
            host (_type_): _description_
            stream_id (_type_): 流id; 创建算法推理任务时返回, 同一个点位同一个解码配置对应一条
            algo_id (_type_): 算法id; 算法包上传时返回
            start_time: 开始时间戳
            end_time: 结束时间戳             
        """
        body = {
            "algo_id": algo_id
        }
        if start_time:
            body["start_time"] = start_time
        if end_time:
            body["end_time"] = end_time 
        if stream_id:
            body["stream_id"] = stream_id    
        log.info(f"invoke {const.API_URLS.DELETE_ALGO_RESULT_BY_TIME_RANGE} {body}")                          
        api = Func.api(host, body=body, **const.API_URLS.DELETE_ALGO_RESULT_BY_TIME_RANGE)
        return api.get_response()       

    @staticmethod
    def get_config_list(host):
        """
        配置中心-查询配置
        :param host: 被测试主机
        :return: dict
            {
            "result": {
                "code": 0,
                "message": ""
            },
            "data":
                [...]
            }

        """
        body = {}
        log.info(f"invoke {const.API_URLS.GET_CONFIG_LIST} {body}")         
        api = Func.api(host, body=body, **const.API_URLS.GET_CONFIG_LIST)
        return api.get_response()

    @staticmethod
    def delete_algo_task(host, algo_id, stream_id=None):
        """
        删除算法任务
        Args:
            host (_type_): _description_
            stream_id (_type_): 流id; 创建算法推理任务时返回, 同一个点位同一个解码配置对应一条
            algo_id (_type_): 算法id; 算法包上传时返回           
        """
        body = {
            "algo_id": algo_id,
            "stream_id": stream_id
        }
        log.info(f"invoke {const.API_URLS.DELETE_ALGO_TASK} {body}")           
        api = Func.api(host, body=body, **const.API_URLS.DELETE_ALGO_TASK)
        return api.get_response()   
    
    @staticmethod
    def delete_camera(host, camera_id):
        """
        删除相机
        Args:
            host (_type_): _description_
            camera_id (_type_): 相机id
        """
        body = {
            "camera_id": camera_id
        }
        log.info(f"invoke {const.API_URLS.DELETE_CAMERA} {body}")    
        api = Func.api(host, body=body, **const.API_URLS.DELETE_CAMERA)
        return api.get_response()      

    @staticmethod
    def delete_app_packet(host, algo_id):
        """
        删除算法包
        Args:
            host (_type_): _description_
            algo_id (_type_): 算法id; 算法包上传时返回           
        """
        body = {
            "algo_id": algo_id
        }
        log.info(f"invoke {const.API_URLS.DELETE_APP_PACKET} {body}")          
        api = Func.api(host, body=body, **const.API_URLS.DELETE_APP_PACKET)
        return api.get_response()    


if __name__ == "__main__":
    print(OpenApi.get_app_packet_list("192.168.101.61:8088"))