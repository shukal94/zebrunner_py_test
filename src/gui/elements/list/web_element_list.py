import logging
import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.exceptions.exceptions import UIException
from src.gui.elements.web_base_element import WebBaseElement


class WebElementList:
    """
    WebElementList return collection of WebElements of given type and with the same locator
    """

    def __init__(self, by, value, wrapper_class):
        """
        WebElementList init method.
        :param by: Locator type, selenium.webdriver.common.by (for example By.XPATH)
        :param value: Locator value (for example "//*[@class='class_name']")
        :param wrapper_class: desirable wrapper (for example WebInput)
        Example:

        # Usage
        1. Click all items in list

        item_buttons = WebElementList(By.XPATH, '//button[@class='item']', WebButton)
        item_buttons_presented = item_buttons.get() # take current items in DOM
        for button in item_buttons_presented: # iterate on buttons array
            button.click()

        2. Find items with specific text inside

        item_buttons = WebElementList(By.XPATH, '//button[@class='item'][contains(text(), '{0}')]', WebButton)
        item_buttons_presented = item_buttons.with_text('DESIRED_TEXT').get() # take current items in DOM
        with specific text inside

        3. Check elements count on page is expected

        item_buttons = WebElementList(By.XPATH, '//button[@class='item']', WebButton)
        item_buttons_with_text = WebElementList(
            By.XPATH, '//button[@class='item'][contains(text(), '{0}')]', WebButton)

        item_buttons_presented_wit_text = item_buttons_with_text.with_text(
            'DESIRED_TEXT').wait_for_count_not_less_than(5)
        item_buttons_presented = item_buttons.wait_for_count_not_more_than(5)


        """
        self.by = by
        self.value = value
        self.wrapper_class = wrapper_class
        self.logger = logging.getLogger('ui')

    def _wrap_elements(self, elements):
        for element in elements:
            element._target_element = WebElement(element.parent, element.id, element._w3c)
            element.__class__ = self.wrapper_class
            element.by = self.by
            element.value = self.value
            element.driver = self.driver

    def __get__(self, obj, owner):
        """
        This method invoked with constructor, and take driver instance from place where it was invoked.
        So, make sure Page Object contains property `driver`
        """
        self.driver = obj.driver
        return self

    def _get_elements(self, condition='presence_of_all_elements_located', wait_time=WebBaseElement.WAIT_TIME):
        array_of_elements = []
        try:
            array_of_elements = WebDriverWait(self.driver, wait_time).until(
                getattr(EC, condition)((self.by, self.value)))  # noqa: E501
        except (NoSuchElementException, TimeoutException, UIException):
            pass  # for situation when we want make sure -length of items is zero
        log_msg = "WebElement array[{0}] with condition [{1}] presented for [{2}:{3}]"
        self.logger.info(log_msg.format(len(array_of_elements), condition, self.by, self.value))

        return array_of_elements

    def get(self, condition='presence_of_all_elements_located', wait_time=WebBaseElement.WAIT_TIME):
        array_of_elements = self._get_elements(condition, wait_time)
        self._wrap_elements(array_of_elements)
        return array_of_elements

    def with_text(self, text=""):
        """
        For dynamic locators, use this method to set text. Value should contains `{0}` inside locator value.
        :param text: text inside web element
        :return:
        """
        self.value = self.value.format(text)
        return self

    def wait_for_count_not_less_than(self, minimal_count, condition='presence_of_all_elements_located',
                                     wait_time=WebBaseElement.WAIT_TIME):
        elements_presented = len(self._get_elements(condition, wait_time))

        minimal_count = int(minimal_count)
        start_time = time.time()
        execution_time = 0
        while (minimal_count > elements_presented) & (execution_time < wait_time):
            elements_presented = len(self._get_elements())
            execution_time = time.time() - start_time
        log_msg = "WebElement array has size[{0}], and expected was [{1}] with condition presented for [{2}:{3}]"

        self.logger.info(log_msg.format(elements_presented, minimal_count, self.by, self.value))
        if minimal_count > elements_presented:
            raise UIException("WebElements count is lower than expected in array")

        return self.get()

    def wait_for_count_not_more_than(self, maximum_count, condition='presence_of_all_elements_located',
                                     wait_time=WebBaseElement.WAIT_TIME):
        elements_presented = len(self._get_elements(condition, wait_time))

        start_time = time.time()
        execution_time = 0
        while (maximum_count < elements_presented) & (execution_time < wait_time):
            elements_presented = len(self._get_elements())
            execution_time = time.time() - start_time
        log_msg = "WebElement array has size[{0}], and expected was [{1}] with condition presented for [{2}:{3}]"

        self.logger.info(log_msg.format(elements_presented, maximum_count, self.by, self.value))
        if maximum_count < elements_presented:
            raise UIException("WebElements count is lower than expected in array")

        return self.get()

    def wait_for_count_to_be(self, expected_count, condition='presence_of_all_elements_located',
                             wait_time=WebBaseElement.WAIT_TIME):
        elements_presented = len(self._get_elements(condition, wait_time))
        expected_count = int(expected_count)
        start_time = time.time()
        execution_time = 0
        while (expected_count != elements_presented) & (execution_time < wait_time):
            elements_presented = len(self._get_elements())
            execution_time = time.time() - start_time
        log_msg = "WebElement array has size[{0}], and expected was [{1}] with condition presented for [{2}:{3}]"

        self.logger.info(log_msg.format(elements_presented, expected_count, self.by, self.value))
        if expected_count != elements_presented:
            raise UIException("WebElements count is not equal to expected in array")

        return self.get()

    def get_all_text_for_elem_list(self):
        text_list = []
        elements = self._get_elements()

        for elem in elements:
            text_list.append(elem.text)
        return text_list
