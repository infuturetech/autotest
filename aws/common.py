
import logging

from contants.global_vars import *
from aws.ssh import ssh_run_cmd_plus

log = logging.getLogger(__name__)

def check_service_is_running(host, service_name):
    """
    检查服务当前状态是否是running
    Args:
        host (_type_): _description_
        service_name (_type_): _description_
    """
    if service_name not in ALL_SERVICE:
        raise Exception(f"错误! {service_name}服务不在有效范围内!")
    cmd = f"systemctl status {service_name}"
    with ssh_run_cmd_plus(host) as _ssh:
        ret = _ssh.run_cmd(cmd, sudo=True)
        log.info(f"\n {ret}")
        if "active (running)" in str(ret):
            return True
        else:
            return False
        

def ctrl_service(host, service_name, ctrl="status"):
    """
    操作服务
    Args:
        host (_type_): _description_
        service_name (_type_): _description_
        ctrl : status/start/stop
    """
    if service_name not in ALL_SERVICE:
        raise Exception(f"错误! {service_name}服务不在有效范围内!")
    log.info(f"{ctrl} {service_name}")  
    if ctrl == "status":
        return check_service_is_running(host, service_name) 
    else:
        cmd = f"systemctl {ctrl} {service_name}"
        with ssh_run_cmd_plus(host) as _ssh:
             _ssh.run_cmd(cmd, sudo=True)


if __name__ == "__main__":
    print(check_service_is_running("192.168.101.61", AMS))     