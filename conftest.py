import os

import urllib3

from zebrunnerpy import connector_obj, PyTestZafiraListener

from src.common.logging_config import apply_initial_logging_configuration

apply_initial_logging_configuration()


pytest_plugins = ['zebrunnerpy.plugin']
is_zafira_plugged_in = True
connector_obj.pytest_listener = PyTestZafiraListener(connector_obj.state)


def pytest_configure(config):
    """
    Attaches wrapped hooks as plugin
    """
    config.pluginmanager.register(connector_obj.pytest_listener)
    os.getcwd()


def pytest_sessionstart(session):
    # basic settings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
