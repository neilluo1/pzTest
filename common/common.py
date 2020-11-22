import re
from utils.util import to_24hour_datetime
from libs.ssh_obj import SSHObj


def get_io_stats(device, ip, username, password, count=1):
    device_name = device.split('/')[-1]
    cmd = "iostat -mxcdt -p {device} -y 1 {count}".format(device=device, count=count)
    ssh_obj = SSHObj(ip, username, password)
    rtn_dict = ssh_obj.run_cmd(cmd)
    io_stats = dict()
    if rtn_dict['rc'] == 0:
        time_pattern = r"\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2}.*\b"
        stdout_list = rtn_dict['stdout'].strip().split('\n')
        for stdout in stdout_list:
            m = re.search(time_pattern, stdout)
            if m:
                time_str = m.group()
                c_time = to_24hour_datetime(time_str)
                io_stats[c_time] = dict()

            if device_name in stdout:
                device_io_stat_list = stdout.split()
                r_iops = int(float(device_io_stat_list[3]))
                w_iops = int(float(device_io_stat_list[4]))
                r_throughput = int(float(device_io_stat_list[5]))
                w_throughput = int(float(device_io_stat_list[6]))
                util = float(device_io_stat_list[-1])

                io_stats[c_time]['r_iops'] = r_iops
                io_stats[c_time]['w_iops'] = w_iops
                io_stats[c_time]['r_throughput'] = r_throughput
                io_stats[c_time]['w_throughput'] = w_throughput
                io_stats[c_time]['util'] = util

    return io_stats
