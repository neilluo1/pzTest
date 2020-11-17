import pytest
from libs.log_obj import LogObj
import datetime
import os
import sys
from benchmark.cases import arguments

sys.setrecursionlimit(100000)
args = arguments.parse_arg()

start_time = datetime.datetime.now()
time_str = start_time.strftime('%Y-%m-%d-%H-%M-%S')

log_file = '{action}-{flag}.log'.format(action=args.action, flag=time_str)
html_name = '{action}-{flag}.html'.format(action=args.action, flag=time_str)

run_list = []
run_list.extend(args.cases)
case = 'benchmark/cases/{action}.py'.format(action=args.action)

logger = LogObj(log_file).get_logger()
run_tests = ' or '.join(run_list)

report_path = os.path.join(os.getcwd().split('storage')[0], 'storage/report/templates/')
if not os.path.exists(report_path):
    os.makedirs(report_path)

html_path = os.path.join(report_path, html_name)

cmd = ['-sv', '--disable-warnings', '--show-capture=no', '--tb=short', '-k {tests}'.format(tests=run_tests), '--count={iteration}'.format(iteration=1), '--repeat-scope=session', '--html={path}'.format(path=html_path), '--self-contained-html', case]

logger.info('Run test command: {cmd}'.format(cmd=cmd))
test_rtn = pytest.main(cmd)

if test_rtn != 0:
    raise Exception('{action} test fail!'.format(action=args.action.upper()))