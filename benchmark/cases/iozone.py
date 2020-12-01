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
    Block size: 4KB, File size: 512MB
    """
    benchmark_obj.iozone_run('-r 4k -s 512m -i 0 -i 1')


def test_case2(benchmark_obj):
    """
    Block size: 128KB, File size: 512MB
    """
    benchmark_obj.iozone_run('-r 128k -s 512m -i 0 -i 1')


def test_case3(benchmark_obj):
    """
    Block size: 512KB, File size: 512MB
    """
    benchmark_obj.iozone_run('-r 512k -s 512m -i 0 -i 1')