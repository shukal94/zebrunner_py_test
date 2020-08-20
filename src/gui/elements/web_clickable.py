import logging

from src.exceptions.exceptions import UIException
from src.gui.elements.web_base_element import WebBaseElement


class WebClickable(WebBaseElement):
    """
    Entity with click methods, not for inheritance, use WebButton and WebLink
    """

    def __init__(self, by, value):
        self.by = by
        self.value = value
        super().__init__(by, value)

    def click(self, wait_time=WebBaseElement.WAIT_TIME):
        """
        Click item or throw exceptions if not visible/presented/enabled
        """
        self.get_element(condition='element_to_be_clickable', wait_time=wait_time).click()
        logging.getLogger('ui').info('WebClickable clicked [{0}:{1}]'.format(self.by, self.value))

    def is_clickable(self, wait_time=0):
        """
        Return True or False, or throw exceptions if not visible/presented/enabled
        """
        try:
            self.get_element(condition='element_to_be_clickable', wait_time=wait_time)
            logging.getLogger('ui').info('WebClickable is clickable [{0}:{1}]'.format(self.by, self.value))
            return True
        except UIException:
            logging.getLogger('ui').info('WebClickable is not clickable [{0}:{1}]'.format(self.by, self.value))
            return False

    def is_not_clickable(self, wait_time=0):
        return not self.is_clickable(wait_time)

    def wait_for_clickable(self, wait_time=WebBaseElement.WAIT_TIME):
        """
        Return True or False after timeout, or throw exceptions if not visible/presented/enabled
        """
        return self.is_clickable(wait_time=wait_time)

    def wait_for_not_clickable(self, wait_time=WebBaseElement.WAIT_TIME):
        return self.is_not_clickable(wait_time=wait_time)

    def click_and_wait_for_disappear(self):
        """
        Return True or throw exceptions if element visible after timeout
        """
        self.click()
        is_not_visible = self.wait_for_not_visible()
        if not is_not_visible:
            raise UIException('WebClickable still visible  [{0}:{1}]'.format(self.by, self.value))
