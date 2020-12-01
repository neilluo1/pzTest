from utils.util import run_cmd
import os
from libs.log_obj import LogObj

logger = LogObj().get_logger()


class benchmarkObj(object):
    def __init__(self, path):
        self.path = path
        self.fs_mark = os.path.join(os.getcwd().split('storage')[0], 'storage/bin/fs_mark')
        self.iozone = os.path.join(os.getcwd().split('storage')[0], 'storage/bin/iozone')

    def fs_mark_run(self, entry):
        cmd = '{bin} -d {path} {entry}'.format(bin=self.fs_mark, path=self.path, entry=entry)
        rtn_dict = run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] is None:
            logger.debug(rtn_dict['stdout'])
        else:
            raise Exception('Run fs_mark entry {entry} failed!'.format(entry=entry))

    def iozone_run(self, entry):
        file_name_path = os.path.join(self.path, 'iozone')
        cmd = '{bin} -f {path} -e -o {entry}'.format(bin=self.iozone, path=file_name_path, entry=entry)
        rtn_dict = run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] is None:
            logger.debug(rtn_dict['stdout'])
        else:
            raise Exception('Run iozone entry {entry} failed!'.format(entry=entry))