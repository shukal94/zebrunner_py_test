import logging

from src.exceptions.exceptions import UIException
from src.gui.elements.web_base_element import WebBaseElement
from src.gui.elements.web_clickable import WebClickable


class WebDropDown(WebClickable):

    def __init__(self, by, value):
        self.by = by
        self.value = value
        super().__init__(by, value)

    def wait_for_selected(self, wait_time=WebBaseElement.WAIT_TIME):
        """
        Return True or False after timeout, no exceptions
        """
        return self.is_selected(wait_time=wait_time)

    def is_selected(self, wait_time=0):
        """
        Return True or False, no exceptions
        """
        try:
            self.get_element(condition='element_located_to_be_selected', wait_time=wait_time)
            logging.getLogger('ui').info('WebElement is selected [{0}:{1}]'.format(self.by, self.value))
            return True
        except UIException:
            logging.getLogger('ui').info('WebElement is not selected [{0}:{1}]'.format(self.by, self.value))
            return False
