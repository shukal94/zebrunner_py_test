# import logging
# import os
#
# import urllib3
#
# from pytest_zafira import RabbitHandler, connector_obj
#
# from pytest_zafira.listeners.pytest_listener import PyTestZafiraListener
#
# from src.common.logging_config import apply_initial_logging_configuration
#
# apply_initial_logging_configuration()
#
# is_zafira_plugged_in = None
#
# if os.environ.get('CI'):
#     pytest_plugins = ['pytest_zafira.plugin']
#     is_zafira_plugged_in = True
#     connector_obj.pytest_listener = PyTestZafiraListener(connector_obj.state)
#
#     def pytest_configure(config):
#         """
#         Attaches wrapped hooks as plugin
#         """
#         config.pluginmanager.register(connector_obj.pytest_listener)
#
#
# def pytest_sessionstart(session):
#     # basic settings
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#     # activate zafira log appender here
#     if is_zafira_plugged_in:
#         rh = RabbitHandler()
#         logging.getLogger("settings").addHandler(rh)
#         logging.getLogger("ui").addHandler(rh)
#         logging.getLogger("test").addHandler(rh)
#         logging.getLogger("zafira").addHandler(rh)


