import datetime
import time
from pyrfc3339 import generate, parse

from contants.global_vars import SSH_USER, SSH_PASSWORD
from aws.ssh import SSH

__all__ = ['get_utc_time', 'utc2bjt', 'get_remote_host_utc_format_time', 'get_remote_host_utc_time',
           'string_time_to_timestamp', 'string_time_to_utc']


def get_remote_host_utc_time(host, is_utc=True):
    ssh = SSH(host.split(':')[0], SSH_USER, SSH_PASSWORD)
    try:
        ssh.conn()
        # 查看1970-01-01 UTC 00:00:00到现在所经过的秒数
        cmd = "date +%s -u"
        if is_utc:
            return float(ssh.run_cmd(cmd)[0]) - 8 * 3600
        else:
            return float(ssh.run_cmd(cmd)[0])     
    except:
        return time.time() - 8 * 3600
    finally:
        if ssh:
            ssh.close()


def get_remote_host_utc_format_time(host):
    ssh = SSH(host.split(':')[0], SSH_USER, SSH_PASSWORD)
    try:
        ssh.conn()
        cmd = 'date +"%Y-%m-%dT%H:%M:%S.%8NZ" -u'
        return ssh.run_cmd(cmd)[0].strip()
    finally:
        if ssh:
            ssh.close()


def get_utc_time(forward_days, forward_mins=0, forward_hours=0, forward_sec=0, now=None):
    """
        获取utc_time类型时间
    :param forward_days:
    :param forward_mins:
    :param forward_hours:
    :return:
    """
    if not now:
        now = datetime.datetime.now()
    if forward_hours and forward_mins:
        new_time = now + datetime.timedelta(
            days=forward_days, hours=forward_hours, minutes=forward_mins)
    elif forward_hours and forward_sec:
        new_time = now + datetime.timedelta(
            days=forward_days, hours=forward_hours, seconds=forward_sec)
    else:
        if forward_hours:
            new_time = now + datetime.timedelta(days=forward_days,
                                                hours=forward_hours)
        elif forward_mins:
            new_time = now + datetime.timedelta(days=forward_days,
                                                minutes=forward_mins)
        elif forward_sec:
            new_time = now + datetime.timedelta(days=forward_days,
                                                seconds=forward_sec)
        else:
            new_time = now + datetime.timedelta(days=forward_days)

    end_time = str(generate(new_time, accept_naive=True, microseconds=True))
    return end_time


def utc2bjt(utct):
    dt = parse(utct)
    bjdt = dt + datetime.timedelta(hours=8)
    return bjdt.strftime("%Y-%m-%d %H:%M:%S %f")


def string_time_to_timestamp(local_time, _format='%Y-%m-%d %H:%M:%S'):
    """将date_time字符串格式时间转换成时间戳;如 2021-07-10 14:20:00 ---->> 1625898014 """
    time_stamp = datetime.datetime.strptime(local_time, _format).timestamp()
    return time_stamp


def string_time_to_utc(local_time, _format='%Y-%m-%d %H:%M:%S'):
    time_stamp = string_time_to_timestamp(local_time, _format)
    utc_time = datetime.datetime.utcfromtimestamp(time_stamp).strftime(
        '%Y-%m-%dT%H:%M:%SZ')
    return utc_time


if __name__ == "__main__":
    playback_min = 4
    _now = datetime.datetime.now()
    for _ in range(0,4):
            forward_sec = 0 + int(_)
            _capture_time = get_utc_time(0, forward_sec=forward_sec, now=_now)
            print(_capture_time)
    # print(get_utc_time(0, forward_sec=-10))
    # print(get_utc_time(0, forward_sec=-8))
    # print(get_utc_time(forward_days=0, forward_hours=0, forward_mins=int(playback_min)))
    # print(get_utc_time(forward_days=0, forward_hours=0, forward_sec=-40))
    # print(string_time_to_utc("2022-10-15 14:00:37"))
    # print(get_remote_host_utc_time("172.20.25.109"))
    print(get_remote_host_utc_time("192.168.101.61", is_utc=False))