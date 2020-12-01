import pytest
from benchmark.common.benchmark_obj import benchmarkObj
from benchmark.cases import arguments
from libs.log_obj import LogObj

logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def benchmark_obj():
    benchmark_obj = benchmarkObj(args.path)

    return benchmark_obj


def test_case1(benchmark_obj):
    """
    File number: 1000, File size: 1M
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000')


def test_case2(benchmark_obj):
    """
    File number: 1000, File size: 1M, NoSync
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000 -S 0')


def test_case3(benchmark_obj):
    """
    File number: 1000, File size: 1M, FsyncBeforeClose
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000 -S 1')


def test_case4(benchmark_obj):
    """
    File number: 1000, File size: 1M, Sync
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000 -S 2')


def test_case5(benchmark_obj):
    """
    File number: 1000, File size: 1M, PostReverseFsync
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000 -S 3')


def test_case6(benchmark_obj):
    """
    File number: 1000, File size: 1M, SyncPostReverseFsync
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000 -S 4')


def test_case7(benchmark_obj):
    """
    File number: 1000, File size: 1M, PostFsync
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000 -S 5')


def test_case8(benchmark_obj):
    """
    File number: 1000, File size: 1M, SyncPostFsync
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 1000 -S 6')


def test_case9(benchmark_obj):
    """
    File number: 5000, File size: 1M, 4threads
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 5000 -t 4')


def test_case10(benchmark_obj):
    """
    File number: 4000, File size: 1M, 32 sub dirs
    """
    benchmark_obj.fs_mark_run('-s 1048576 -n 4000 -D 32')