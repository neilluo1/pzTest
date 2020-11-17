import pytest
from benchmark.fs_mark_obj import fsMarkObj
from benchmark.cases import arguments
from libs.log_obj import LogObj

logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def fs_mark_obj():
    fs_mark_obj = fsMarkObj(args.path)

    return fs_mark_obj


def test_100File_1M(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 100')


def test_100File_1M_NoSync(fs_mark_obj):
    fs_mark_obj.run('-s 1048576 -n 100 -S 0')
