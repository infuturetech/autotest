
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
