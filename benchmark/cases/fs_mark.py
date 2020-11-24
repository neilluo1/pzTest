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


def test_case1(fs_mark_obj):
    """
    File number: 1000, File size: 1M
    """
    fs_mark_obj.run('-s 1048576 -n 1000')


def test_case2(fs_mark_obj):
    """
    File number: 1000, File size: 1M, NoSync
    """
    fs_mark_obj.run('-s 1048576 -n 1000 -S 0')


def test_case3(fs_mark_obj):
    """
    File number: 1000, File size: 1M, FsyncBeforeClose
    """
    fs_mark_obj.run('-s 1048576 -n 1000 -S 1')


def test_case4(fs_mark_obj):
    """
    File number: 1000, File size: 1M, Sync
    """
    fs_mark_obj.run('-s 1048576 -n 1000 -S 2')


def test_case5(fs_mark_obj):
    """
    File number: 1000, File size: 1M, PostReverseFsync
    """
    fs_mark_obj.run('-s 1048576 -n 1000 -S 3')


def test_case6(fs_mark_obj):
    """
    File number: 1000, File size: 1M, SyncPostReverseFsync
    """
    fs_mark_obj.run('-s 1048576 -n 1000 -S 4')


def test_case7(fs_mark_obj):
    """
    File number: 1000, File size: 1M, PostFsync
    """
    fs_mark_obj.run('-s 1048576 -n 1000 -S 5')


def test_case8(fs_mark_obj):
    """
    File number: 1000, File size: 1M, SyncPostFsync
    """
    fs_mark_obj.run('-s 1048576 -n 1000 -S 6')


def test_case9(fs_mark_obj):
    """
    File number: 5000, File size: 1M, 4threads
    """
    fs_mark_obj.run('-s 1048576 -n 5000 -t 4')


def test_case10(fs_mark_obj):
    """
    File number: 4000, File size: 1M, 32 sub dirs
    """
    fs_mark_obj.run('-s 1048576 -n 4000 -D 32')