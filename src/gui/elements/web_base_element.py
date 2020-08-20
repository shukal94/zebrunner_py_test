import logging
import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.exceptions.exceptions import UIException


class WebBaseElement:
    """
    WebElement is basic object, that represents any item in the DOM of the page, and able to interact with it.
    It's base element with common methods for all elements. In most cases better to use his childs in PageObjects
    """
    WAIT_TIME = 15

    def __init__(self, by, value):
        """
        WebElement init method. Use `selenium.webdriver.common.by import By` and string value.
        Example: close_chat_window_button = WebButton(By.CLASS_NAME, 'asappChatSDKBadge_opened')
        """
        self.by = by
        self.value = value
        self.unmutable_locator = value
        self._target_element = None

    def __get__(self, obj, owner):
        """
        This method invoked with constructor, and take driver instance from place where it was invoked.
        So, make sure Page Object contains property `driver`
        """
        self.driver = obj.driver
        return self

    def __repr__(self):
        return self.value

    def with_text(self, text=""):
        """
        For dynamic locators, use this method to set text. Value should contains `{0}` inside locator value.
        """
        self.value = self.unmutable_locator.format(text)
        return self

    def get_element(self, condition='presence_of_element_located', wait_time=WAIT_TIME):
        """
        When called, driver starts actual search of element on page, normally won't be called directly
        """
        if self._target_element:
            element = self._target_element
            return element
        try:
            element = WebDriverWait(self.driver, wait_time).until(getattr(EC, condition)((self.by, self.value)))
            logging.getLogger('ui').info(
                'WebElement with condition [{0}] presented for [{1}:{2}]'.format(condition, self.by, self.value))
            return element
        except Exception:
            raise UIException(
                'WebElement with condition [{0}] NOT presented for [{1}:{2}]'.format(condition, self.by, self.value))

    def is_visible(self, wait_time=0):
        """
        Return True or False, no exceptions
        """
        try:
            self.get_element(condition='visibility_of_element_located', wait_time=wait_time)
            logging.getLogger('ui').info('WebElement is visible [{0}:{1}]'.format(self.by, self.value))
            return True
        except UIException:
            logging.getLogger('ui').info('WebElement is not visible [{0}:{1}]'.format(self.by, self.value))
            return False

    def is_not_visible(self, wait_time=0):
        """
        Return True or False, no exceptions
        """
        try:
            self.get_element(condition='invisibility_of_element_located', wait_time=wait_time)
            logging.getLogger('ui').info('WebElement is not visible [{0}:{1}]'.format(self.by, self.value))
            return True
        except UIException:
            logging.getLogger('ui').info('WebElement is visible [{0}:{1}]'.format(self.by, self.value))
            return False

    def wait_for_visible(self, wait_time=WAIT_TIME):
        """
        Return True or False after timeout, no exceptions
        """
        return self.is_visible(wait_time=wait_time)

    def wait_for_not_visible(self, wait_time=WAIT_TIME):
        """
        Return True or False after timeout, no exceptions
        """
        return self.is_not_visible(wait_time=wait_time)

    def wait_text_not_empty(self, wait_time=WAIT_TIME):
        """
        Wait text to be not empty, in other case will raise Exception
        """
        start_time = time.time()
        execution_time = 0
        element_text = ""
        while (element_text == "") & (execution_time < wait_time):
            element_text = self.get_text()
            execution_time = time.time() - start_time

        if element_text == "":
            raise UIException("WebElement is still empty [{0}:{1}]".format(self.by, self.value))

    def wait_text_equals(self, expected_text, wait_time=WAIT_TIME):
        """
        Wait text to be not empty, in other case will raise Exception
        """
        start_time = time.time()
        execution_time = 0
        element_text = ""
        while (str(element_text) != str(expected_text)) & (execution_time < wait_time):
            element_text = self.get_text()
            execution_time = time.time() - start_time

        if str(element_text) != str(expected_text):
            raise UIException(
                "WebElement text not changed from [{0}] to [{1}] [{2}:{3}]".format(
                    element_text, expected_text, self.by, self.value))

    def wait_text_not_equal(self, not_expected_text, wait_time=WAIT_TIME):
        """
        Wait text to be not equal provided value, in other case will raise Exception
        """
        start_time = time.time()
        execution_time = 0
        element_text = ""
        while (str(element_text) == str(not_expected_text)) & (execution_time < wait_time):
            element_text = self.get_text()
            execution_time = time.time() - start_time

        if str(element_text) == str(not_expected_text):
            raise UIException(
                "WebElement text not changed from [{0}] to [{1}] [{2}:{3}]".format(element_text, not_expected_text,
                                                                                   self.by,
                                                                                   self.value))

    def wait_css_property_changed_from(self, property_name, not_expected_property_value, wait_time=WAIT_TIME):
        """
        Wait text to be not equal provided value, in other case will raise Exception
        """
        start_time = time.time()
        execution_time = 0
        element_property = self.get_css_property(property_name)
        while (str(element_property) == str(not_expected_property_value)) & (execution_time < wait_time):
            element_property = self.get_css_property(property_name)
            execution_time = time.time() - start_time

        if str(element_property) == str(not_expected_property_value):
            raise UIException(
                "WebElement css property [{0}] not changed from [{1}] to [{2}] [{3}:{4}]".format(property_name,
                                                                                                 element_property,
                                                                                                 not_expected_property_value,  # noqa: E501
                                                                                                 self.by,
                                                                                                 self.value))

    def get_text(self):
        """
        Return element text, or throw exception if no element presented
        """
        element_with_text = self.get_element()
        for retry in range(0, 3):
            try:
                text_in_element = element_with_text.text
                break
            except StaleElementReferenceException:
                logging.getLogger('ui').debug('WebElement text getting failed for [{1}:{2}], retry {3}'.format(
                    self.by, self.value, retry))

        logging.getLogger('ui').info('WebElement text is {0} for [{1}:{2}]'.format(text_in_element,
                                                                                   self.by, self.value))
        return text_in_element

    def get_attribute(self, attribute_name):
        """
        Return element's attribute, or throw exception if no element presented or now attribute
        """
        element = self.get_element()

        attribute_value = element.get_attribute(attribute_name)
        if not attribute_value:
            attribute_value = getattr(element, attribute_name)
            logging.getLogger('ui').info(
                'WebElement attribute [{0}:{1}] for [{2}:{3}]'.format(attribute_name, attribute_value,
                                                                      self.by, self.value))
        return attribute_value

    def get_attribute_of_nth_parent_element(self, parent_tag, n, attribute_name):
        element = self.get_element()
        for i in range(n):
            element.value += '/parent::{parent_tag}'.format(parent_tag=parent_tag)
        attribute_value = element.get_attribute(attribute_name)
        if not attribute_value:
            attribute_value = getattr(element, attribute_name)
            logging.getLogger('ui').info(
                'WebElement attribute [{0}:{1}] for [{2}:{3}]'.format(attribute_name, attribute_value,
                                                                      element.by, element.value))
        return attribute_value

    def get_css_property(self, property_name):
        element = self.get_element()

        property_value = element.value_of_css_property(property_name)
        if not property_value:
            property_value = getattr(element, property_name)
            logging.getLogger('ui').info(
                'WebElement css attribute [{0}:{1}] for [{2}:{3}]'.format(property_name, property_value,
                                                                          self.by, self.value))
        return property_value

    def move_by_offset(self, xoffset, yoffset):
        """
        Move the element by clicking and dragging to the specified x and y coordinates
        :param xoffset:  X offset in pixels to move the mouse.
        :param yoffset:  Y offset in pixels to move the mouse.
        :return: None
        """
        move = AC(self.driver)
        element = self.get_element()
        move.click_and_hold(element).move_by_offset(xoffset, yoffset).release().perform()

    def move_to(self):
        hover_action = AC(self.driver)
        element = self.get_element()
        hover_action.move_to_element(element).perform()
        return element

    @property
    def size(self):
        """The size of the element."""
        element = self.get_element()
        size = element.size
        logging.getLogger('ui').info(
            'WebElement size [{0}:{1}] for [{2}:{3}]'.format(size["height"], size["width"], self.by, self.value))
        return size

    @property
    def location(self):
        """The location of the element in the renderable canvas."""
        element = self.get_element()
        location = element.location
        logging.getLogger('ui').info(
            'WebElement location [{0}:{1}] for [{2}:{3}]'.format(location['x'], location['y'], self.by, self.value))
        return location
