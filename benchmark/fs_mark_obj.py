from utils.util import run_cmd
import os


class fsMarkObj(object):
    def __init__(self, path):
        self.path = path
        self.fs_mark = os.path.join(os.getcwd().split('storage')[0], 'storage/bin/fs_mark')

    def run(self, entry):
        cmd = '{bin} -d {path} {entry}'.format(bin=self.fs_mark, path=self.path, entry=entry)
        rtn_dict = run_cmd(cmd)
        print(rtn_dict)