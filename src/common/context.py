import configparser
from enum import Enum
from os import getcwd

GUI_CONFIG_FILE_PATH = getcwd() + '/gui_properties.ini'


class Context:

    @staticmethod
    def get_gui_parameter(parameter):
        config = configparser.ConfigParser()
        config.read(GUI_CONFIG_FILE_PATH)
        return config.get('config', parameter.value)


class Parameter(Enum):
    BASE_URL = 'base_url'
    BROWSER = 'browser'
    SELENIUM_HOST = 'selenium_host'
    WAIT = 'wait'
    # chrome options
    NO_SANDBOX = 'no_sandbox'
    DISABLE_LOGGING = 'disable_logging'
    CACHE_SIZE = 'cache_size'
    DISABLE_DEFAULT_APPS = 'disable_default_apps'
    MUTE_AUDIO = 'mute_audio'
    BWSI = 'bwsi'
    IGNORE_CERT_ERRORS = 'ignore_cert_errors'
    NO_FIRST_RUN = 'no_first_run'
    # driver pool settings
    MAX_DRIVERS_COUNT = 'max_drivers_count'
