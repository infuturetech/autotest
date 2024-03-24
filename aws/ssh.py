# -*- coding: utf-8 -*-
import os
import paramiko
import asyncssh
import asyncio
import json
from fabric import Connection
from contextlib import contextmanager
from contants.global_vars import SSH_USER, SSH_PASSWORD, SUDO_PWD


__all__ = ['SSH', 'AsyncSSH', 'inquire_server_run_node_ip', 'Client', 'ssh_run_cmd_plus', "is_ssh_rsa", "ssh_key_rsa", "enable_ssh_rsa"]

DEBUG = False

class SSH:
    def __init__(self, ip, user=SSH_USER, password=SSH_PASSWORD, port=22):
        self.ip = ip.split(":")[0]
        self.user = user
        self.password = password
        self.ssh = None
        self.stdin = None
        self.stderr = None
        self.stdout = None
        self.port = port
        self.pkey = None        

    def conn(self):
        for _ in range(0, 5):
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                # https://blog.csdn.net/weixin_43749427/article/details/109240449?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link
                self.ssh.connect(
                    self.ip,
                    username=self.user,
                    password=self.password,
                    timeout=_ + 10,
                    port=self.port,
                    allow_agent=False,
                    look_for_keys=False,
                    banner_timeout=60,
                    pkey=self.pkey
                )
            except Exception as e:
                print(f"主机{self.ip}连接异常! {e}")
                self.ssh = None
                if _ == 4:
                    ssh_mode = os.environ.get("ssh_mode")
                    raise Exception(f"主机{self.ip}连接重试{_ + 1}次后依然异常! {e}, ssh_mode: {ssh_mode}")
            if self.ssh:
                break
            print(f"{self.ip}连接失败! 重试{_ + 1}次")

    def run(self, cmd, timeout=60 * 10, sudo=False):
        # print(cmd)
        if self.ssh:
            if sudo:
                cmd = "sudo -S -p '' %s" % cmd              
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
            if sudo:
                stdin.write(SUDO_PWD + "\n")
                stdin.flush()                
            self.stdin = stdin
            self.stderr = stderr
            self.stdout = stdout
            return stdout
        else:
            return '%s@%s:%s ssh connect failed!' % (self.ip, self.user, self.password)

    def run_cmd(self, cmd, time_out=600, sudo=False):
        # 新增的run方法，返回值直接是列表，每行对应linux的输出；替代上面的run方法
        # time_out 默认 600s， 可以自定义
        # print(cmd)
        if self.ssh:
            if sudo:
                cmd = "sudo -S -p '' %s" % cmd                  
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=time_out)
            if sudo:
                stdin.write(SUDO_PWD + "\n")
                stdin.flush()              
            self.stdin = stdin
            self.stderr = stderr
            self.stdout = stdout
            return [elem[:-1] if elem[-1] in ['\n', '\t'] else elem[:] for elem in stdout.readlines()]
        else:
            return []

    def run_cmd_stderr(self, cmd, timeout=60 * 10, sudo=False):
        # 新增的run方法，返回值直接是列表，每行对应linux的输出返回stderr的输出
        if self.ssh:
            if sudo:
                cmd = "sudo -S -p '' %s" % cmd                
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
            if sudo:
                stdin.write(SUDO_PWD + "\n")
                stdin.flush()            
            self.stdin = stdin
            self.stderr = stderr
            self.stdout = stdout
            return [elem[:-1] if elem[-1] in ['\n', '\t'] else elem[:] for elem in stderr.readlines()]
        else:
            return []

    def run_cmd_out_stderr(self, cmd, timeout=60 * 10, sudo=False):
        """
         返回命令行的执行结果返回值&错误 一般都是二选一有值
        :param cmd:
        :param timeout:
        :return:
        """
        if self.ssh:
            if sudo:
                cmd = "sudo -S -p '' %s" % cmd            
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
            if sudo:
                stdin.write(SUDO_PWD + "\n")
                stdin.flush()

            self.stdin = stdin
            self.stderr = stderr
            self.stdout = stdout
            out = [elem[:-1] if elem[-1] in ['\n', '\t'] else elem[:] for elem in stdout.readlines()]
            error = [elem[:-1] if elem[-1] in ['\n', '\t'] else elem[:] for elem in stderr.readlines()]
            return out, error
        else:
            return [], []

    def run_status(self, cmd, log=None):
        # 返回执行命令的状态
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=60 * 10)
            stderr_info = stderr.readlines()
            if stderr_info:
                log.info("run cmd=%s failed!! Error info was %s" % (cmd, stderr_info))
                return False
            return True
        else:
            log.info('%s@%s:%s ssh connect failed!' % (self.ip, self.user, self.password))
            return False

    def connect_withtrans(self, port):
        # 连接一个trans 通道， 用来上传和下载文件
        transport = paramiko.Transport(self.ip + ':' + str(port))
        transport.connect(username=self.user, password=self.password, pkey=self.pkey)
        self.__transport = transport
        return transport

    def upload_file(self, local_path, remote_path, port=22):
        # 向远程服务器上传一个文件
        self.connect_withtrans(port)

        # sftp.chmod(target_path, 0o755)
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, remote_path, confirm=True)
        sftp.chmod(remote_path, 0o755)
        sftp.close()

    def download_file(self, remote_path, local_path, port=22):
        # 向远程服务器下载一个文件
        self.connect_withtrans(port)
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)
        sftp.close()

    def close(self):
        if self.ssh:
            self.ssh.close()


class AsyncSSH:
    def __init__(self, ip, user=SSH_USER, password=SSH_PASSWORD):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh = None
        self.ssh_options = None    

    async def conn(self):

        self.ssh = await asyncssh.connect(self.ip, username=self.user, password=self.password, known_hosts=None, options=self.ssh_options)

    async def run_cmd(self, cmd, retry=30):
        try:
            if not self.ssh:
                await self.conn()
            result = await self.ssh.run(cmd, check=True)
            # print(cmd)
            return result.stdout.splitlines()
        except Exception as e:
            if retry == 0:
                raise e
            await asyncio.sleep(0.1)
            return await self.run_cmd(cmd, retry - 1)


class Client(Connection):
    """
    Usage:
        client = Client("172.20.25.111")
        with client.cd("/usr/local"):
            result = client.run("ls -l")

        using the object as a conetxtmanager::
            with Client("172.20.25.111") as client:
                result = client.run("ls")

        download files
        client.get(remote, local)

        upload files
        client.put(local, remote)
    """

    def __init__(self, host, user=SSH_USER, password=SSH_PASSWORD, port=22, **kwargs):
        connect_kwargs = kwargs.get("connect_kwargs", {})
        if connect_kwargs:
            kwargs.pop("connect_kwargs")
        connect_kwargs.update({"password": password})
        super().__init__(host=host.split(":")[0], user=user, connect_kwargs=connect_kwargs, port=port, **kwargs)

    def get_stdout(self, command, **kwargs):
        self.open()
        _, out, _ = self.client.exec_command(command, **kwargs)
        return out.read().decode()


@contextmanager
def ssh_run_cmd_plus(host, ssh_user=SSH_USER, ssh_password=SSH_PASSWORD):
    ssh = SSH(host.split(':')[0], ssh_user, ssh_password)
    try:
        ssh.conn()
        yield ssh
    finally:
        ssh.close()


if __name__ == "__main__":
    with ssh_run_cmd_plus("192.168.101.61") as _ssh:
        print(_ssh.run_cmd("ls"))
        # print(_ssh.run_cmd("docker ps", sudo=True))
        print(_ssh.run_cmd("systemctl status cms.service", sudo=True))        