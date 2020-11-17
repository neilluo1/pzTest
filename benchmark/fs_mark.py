from utils.util import run_cmd
import os


class fsMarkObj(object):
    def __init__(self, path):
        self.path = path
        self.fs_mark = os.path.join(os.getcwd().split('storage')[0], 'storage/bin/fs_mark')

    @property
    def entrys(self):
        entrys = ['-s 1048576 -n 1000', '-s 1048576 -n 1000 -S 0']

    def run(self):
        for entry in self.entrys:
            cmd = '{bin} -d {path} {entry}'.format(bin=self.fs_mark, path=self.path, entry=entry)
            rtn_dict = run_cmd(cmd)
            print(rtn_dict)


if __name__ == '__main__':
    fs_mark_obj = fsMarkObj('/mnt/data/fs_mark/')
    fs_mark_obj.run()