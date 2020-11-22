import subprocess
import traceback
import socket
import time
import datetime
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA
from libs.log_obj import LogObj

logger = LogObj().get_logger()


def run_cmd(cmd):
    """
    create a sub process and run commands --subprocess
    :param cmd:
    :return:(dict) cmd return info
    """

    logger.debug('Subprocess.check_output: {cmd}'.format(cmd=cmd))
    rtn_dict = {'rc': 0, 'stdout': None, 'stderr': None}
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        rtn_dict['stdout'] = result.decode('UTF-8', "ignore")
    except subprocess.CalledProcessError as error:
        rtn_dict['stderr'] = error.output.decode('UTF-8', "ignore")
        rtn_dict['rc'] = error.returncode
    except Exception:
        logger.error('Exception occurred: {err}'.format(err=traceback.format_exc()))
        rtn_dict['rc'] = -1

    return rtn_dict


def get_localhost_ip():
    try:
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_obj.connect(('8.8.8.8', 80))
        ip = socket_obj.getsockname()[0]
    finally:
        socket_obj.close()

    return ip


def to_24hour_datetime(st, fmt='%m/%d/%Y %I:%M:%S %p'):
    """
    Convert a 12-hour time and "am" or "pm" str to a 24-hour datetime value
    04/16/2020 01:52:11 PM  ->  %m/%d/%Y %I:%M:%S %p
    04/16/20 21:52:11  ->  %m/%d/%y %I:%M:%S

    :param st:
    :param fmt:
    :return:
    """

    return datetime.strptime(st, fmt)


def str_to_datetime(st, fmt="%a %b %d %H:%M:%S PST %Y"):
    """
    Convert a str time to a datetime value
    Wed Apr 15 23:20:40 PDT 2020  --> %a %b %d %H:%M:%S PST %Y
    :param st:
    :param fmt:
    :return:
    """
    return datetime.strptime(st, fmt)


def datetime_to_str(st, fmt="%a %b %d %H:%M:%S PST %Y"):
    """
    Convert a datetime to a str time value
    Wed Apr 15 23:20:40 PDT 2020  --> %a %b %d %H:%M:%S PST %Y
    :param st:
    :param fmt:
    :return:
    """
    return st.strftime(fmt)


def sleep(sleep_time):
    """
    Print a progress bar, total value: sleep_time(seconds)
    :param sleep_time:
    :return:
    """

    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')), ' ', ETA()]
    progress_bar = ProgressBar(widgets=widgets, maxval=sleep_time).start()
    for i in range(sleep_time):
        progress_bar.update(1 * i + 1)
        time.sleep(1)
    progress_bar.finish()