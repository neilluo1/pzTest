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
    Block size: 4KB, Min file size: 512MB, Max file size: 4GB
    """
    benchmark_obj.iozone_run('-r 4k -n 512m -g 4g -i 0 -i 1')
