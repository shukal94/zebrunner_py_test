import logging

from selenium.webdriver.common.keys import Keys

from src.exceptions.exceptions import UIException
from src.gui.elements.web_clickable import WebClickable


class WebInput(WebClickable):

    def __init__(self, by, value):
        self.by = by
        self.value = value
        super().__init__(by, value)

    def clear(self):
        """
        Clear input, throw exception if fails or no elements presented
        """
        element_to_clear = self.get_element()
        element_to_clear.clear()
        logging.getLogger('ui').info('WebInput is cleared [{0}:{1}]'.format(self.by, self.value))

    def append(self, text):
        """
        Do not clear input, just append text, throw exception if fails or no elements presented
        """
        element_to_add = self.get_element()
        element_to_add.send_keys(text)
        logging.getLogger('ui').info('WebInput text set to [{0}] for [{1}:{2}]'.format(text, self.by, self.value),
                                     self.by, self.value)

    def set(self, text):
        """
        Clear input and set text, throw exception if fails or no elements presented
        """
        self.clear()
        self.append(text)

    def set_and_check(self, text):
        """
        Clear input and set text, throw exception if fails or no elements presented,
        and if input text is not equals to desired
        """
        self.set(text)
        actual_text = self.get_text()
        if text != actual_text:
            raise UIException(
                'WebInput text [{0}] != [{1}] for [{2}:{3}]'.format(text, actual_text, self.by, self.value))
        else:
            return True

    def upload_file(self, file_path):
        elem = self.get_element()
        if elem:
            elem.send_keys(file_path)

    def press_keys(self, keyname):
        """
        Send keys to webinput.
        Keyname is a key-lookup.  Dictionary key == selenium Keys.FOO command.
        :param keyname:  String name of key to send to element.
        :return: Boolean
        """
        element = self.get_element()
        keys = {
            'enter': Keys.RETURN,
            'esc': Keys.ESCAPE,
            'control': Keys.CONTROL,
            'delete': Keys.DELETE,
            'back_space': Keys.BACK_SPACE
        }

        key = keys.get(keyname)
        if element and key:
            element.send_keys(key)
            logging.getLogger('ui').debug('WebInput key [{0}] sent'.format(keyname))
            return True
        logging.getLogger('ui').warning('WebInput key [{0}] NOT sent'.format(keyname))
        return False

    def set_with_js(self, text):
        element_to_add = self.get_element()
        self.driver.execute_script("arguments[0].value = '" + text + "'", element_to_add)
        logging.getLogger('ui').info('Copy pasting WebInput text set to [{0}] for [{1}:{2}]'.format(
            text, self.by, self.value))
