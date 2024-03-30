
import logging
import os

from contants.global_vars import *
from aws.ssh import ssh_run_cmd_plus
from resources import test_algo_app_file
from contants.global_vars import test_app_server_path, installer_path

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


def upload_app_file_to_server(host, local_app_file=test_algo_app_file):
        """
        将测试app包上传到盒子
        Args:
            host (_type_): _description_
            local_app_file (_type_, optional): _description_. Defaults to test_algo_app_file.
        """
        print(f"将测试算法包{local_app_file}上传到{test_app_server_path}")
        with ssh_run_cmd_plus(host) as _ssh:
            _ssh.upload_file(local_app_file, f"{test_app_server_path}/{os.path.basename(local_app_file)}")
            log.info(f"将测试算法包{local_app_file}上传完成")

            return f"{test_app_server_path}/{os.path.basename(local_app_file)}"


def do_recv_algo_result_call_back(host, command="start"):
    """
    模拟接收回调结果
    Args:
        host (_type_): _description_
        command (str, optional): _description_. Defaults to "start".
    """
    save_log_file = "/tmp/recv_callback.txt"
    def get_recv_pid(_ssh):
        cmd = "ps -elf | grep 'client rcv' | grep -v 'grep' | awk '{print $4}'"
        ppid = _ssh.run_cmd(cmd)
        log.info(f"回调监听进程id: {ppid}")
        return ppid
    
    with ssh_run_cmd_plus(host) as _ssh:
        if command == "start":
            _pid = get_recv_pid(_ssh)
            if _pid:
                _ssh.run_cmd(f"kill {_pid[0]}")
            _ssh.run_cmd(f"rm -rf {save_log_file}")
            _c = f'cd {installer_path}/output/client; ./client  rcv algoresult > {save_log_file} & '
            log.info(_c)
            log.info(_ssh.run_cmd(_c))
            log.info(f"start pid: {get_recv_pid(_ssh)}")
        else:
            _pid = get_recv_pid(_ssh)
            if _pid:
                _ssh.run_cmd(f"kill {_pid[0]}")           
            ret = _ssh.run_cmd(f"cat {save_log_file} | head -n 2")

            return ret


if __name__ == "__main__":
    # print(check_service_is_running("192.168.101.61", AMS))   
    upload_app_file_to_server("192.168.101.61") 