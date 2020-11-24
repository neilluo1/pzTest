import pytest
from py._xmlgen import html
from datetime import datetime
import pytz


def pytest_configure(config):
    config._metadata['Author'] = 'Neil'


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Start Time'))
    cells.insert(2, html.th('Description'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.start_time))
    cells.insert(2, html.td(report.description))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    report.start_time = datetime.now(tz=pytz.timezone('US/Pacific'))
    report.description = str(item.function.__doc__)