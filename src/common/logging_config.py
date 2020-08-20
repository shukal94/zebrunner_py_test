import logging.config
import os
import yaml


def apply_initial_logging_configuration():
    path = os.getcwd()
    config = yaml.load(open(os.path.join(path, 'logging.cfg'), 'r'))
    logging.config.dictConfig(config)
