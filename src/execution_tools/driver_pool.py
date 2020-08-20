import logging

from src.common.context import Parameter, Context
from src.execution_tools.make_driver import BaseDriver


class DriverPool:

    MAX_DRIVERS_COUNT = int(Context.get_gui_parameter(Parameter.MAX_DRIVERS_COUNT))

    LOGGER = logging.getLogger('settings')

    def __init__(self, drivers_count=1):
        self.drivers = list()
        self.drivers_count = drivers_count

    def init_drivers(self):
        for _ in range(self.drivers_count):
            self.create_driver()

    def get_driver(self, index=0):
        if self.drivers.__len__() == 0:
            self.LOGGER.debug('Driver pool is empty. Will create a new driver')
            self.create_driver()

        try:
            return self.drivers[index]
        except IndexError as e:
            self.LOGGER.error(e)
            return self.drivers[0]

    def create_driver(self):
        driver = BaseDriver().driver

        self.drivers.append(driver)

        assert len(self.drivers) <= self.MAX_DRIVERS_COUNT, 'Max driver pool length is reached.'
        self.LOGGER.debug('Driver is on the pool.')
        return driver

    def kill_drivers(self):
        self.LOGGER.debug('Will kill drivers. Drivers count: {}'.format(len(self.drivers)))
        for driver in self.drivers:
            driver.quit()
