import logging
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from src.common.context import Parameter, Context


class BaseDriver:
    def __init__(self):
        """
        Base Selenium Driver for tests.
        :return: None
        """

        wait = Context.get_gui_parameter(Parameter.WAIT)
        browser = Context.get_gui_parameter(Parameter.BROWSER)
        command_executor = Context.get_gui_parameter(Parameter.SELENIUM_HOST)

        self.driver = make_driver(browser, command_executor)

        self.set_wait(wait)
        self.driver.maximize_window()

    def set_wait(self, wait):
        """
        Sets the implicit wait time.
        :param wait:  Wait time, type int().  Set in `gui_properties.ini`
        :return: None
        """
        self.driver.implicitly_wait(wait)


def make_driver(browser, command_executor):
    """
    Instantiates the remote webdriver browser.
    Points the driver to the provided command_executor address.
    :param browser:  Type string.  Browser type to instantiate.
    :return:  Instantiated remote driver.
    """
    if browser == 'chrome':
        opts = Options()
        opts_from_config = [
            Context.get_gui_parameter(Parameter.BWSI),
            Context.get_gui_parameter(Parameter.CACHE_SIZE),
            Context.get_gui_parameter(Parameter.DISABLE_DEFAULT_APPS),
            Context.get_gui_parameter(Parameter.DISABLE_LOGGING),
            Context.get_gui_parameter(Parameter.IGNORE_CERT_ERRORS),
            Context.get_gui_parameter(Parameter.MUTE_AUDIO),
            Context.get_gui_parameter(Parameter.NO_FIRST_RUN),
            Context.get_gui_parameter(Parameter.NO_SANDBOX)
        ]

        for option in opts_from_config:
            opts.add_argument(option)
        caps = opts.to_capabilities()
    elif browser == 'firefox':
        caps = DesiredCapabilities.FIREFOX
    else:
        raise ValueError('Out of options, should not be here!')
    logging.info('*')  # workaround for better logging format
    logging.info('Driver was created.\nBrowser: {browser},\ncapabilities: {caps}'
                 .format(browser=browser, caps=caps.__repr__()))
    return webdriver.Remote(desired_capabilities=caps, command_executor=command_executor)
