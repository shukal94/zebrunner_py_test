from selenium.webdriver.common.by import By

from src.gui.elements.web_base_element import WebBaseElement
from src.gui.pages.base_page import BasePage


class GoogleSearchResultsPage(BasePage):
    main_logo = WebBaseElement(By.XPATH, '//div[contains(@class, "logo")]')

    def __init__(self, driver):
        super().__init__(driver)

    def is_page_opened(self):
        return self.main_logo.is_visible()
