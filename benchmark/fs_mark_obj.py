from utils.util import run_cmd
import os
from libs.log_obj import LogObj

logger = LogObj().get_logger()


class fsMarkObj(object):
    def __init__(self, path):
        self.path = path
        self.fs_mark = os.path.join(os.getcwd().split('storage')[0], 'storage/bin/fs_mark')

    def run(self, entry):
        cmd = '{bin} -d {path} {entry}'.format(bin=self.fs_mark, path=self.path, entry=entry)
        rtn_dict = run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] is None:
            logger.debug(rtn_dict['stdout'])
        else:
            raise Exception('Run entry {entry} failed!'.format(entry=entry))