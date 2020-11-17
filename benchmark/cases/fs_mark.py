import pytest
from benchmark.common.fs_mark_obj import fsMarkObj
from benchmark.cases import arguments
from libs.log_obj import LogObj

logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def fs_mark_obj():
    fs_mark_obj = fsMarkObj(args.path)

    return fs_mark_obj


def test_1000files_1M(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000')


def test_1000files_1M_noSync(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000 -S 0')


def test_1000files_1M_fsyncBeforeClose(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000 -S 1')


def test_1000files_1M_sync(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000 -S 2')


def test_1000files_1M_postReverseFsync(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000 -S 3')


def test_1000files_1M_syncPostReverseFsync(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000 -S 4')


def test_1000files_1M_postFsync(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000 -S 5')


def test_1000files_1M_syncPostFsync(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 1000 -S 6')


def test_5000files_1M_4threads(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 5000 -t 4')


def test_4000files_1M_32sub_dirs(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 4000 -D 32')