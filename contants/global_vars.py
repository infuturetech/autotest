
SSH_USER = "nvidia"
SSH_PASSWORD = "nvidia"

SUDO_PWD = SSH_PASSWORD

# 服务名称
AMS = "ams.service"
CMS = "cms.service"
IMS = "ims.service"
MCS = "mcs.service"
GATEWAY = "gateway.service"
SMS = "sms.service"
VIS = "vis.service"
VPS = "vps.service"

ALL_SERVICE = [AMS, CMS, IMS, MCS, GATEWAY, SMS, VIS, VPS]

# ffmpeg -re  -stream_loop -1  -i girls.mp4   -vcodec copy -acodec copy  -rtsp_transport tcp   -f rtsp rtsp://127.0.0.1:8554/test
rtsp_1k = "rtsp://127.0.0.1:8554/test"

rtsp_2k = "rtsp://127.0.0.1:8554/test"

rtsp_4k = "rtsp://127.0.0.1:8554/test"

# 测试app包存储于盒子端的路径
test_app_server_path = "/home/nvidia/test_app"

# 测试工具mock监听回调接口
mock_callback_api = "http://127.0.0.1:9988/callback"


installer_path = "/home/nvidia/infuturetech/installer"
