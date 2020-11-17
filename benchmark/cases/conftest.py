import pytest


def pytest_configure(config):
    config._metadata['Author'] = 'Neil'
