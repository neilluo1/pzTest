import subprocess
import traceback
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
