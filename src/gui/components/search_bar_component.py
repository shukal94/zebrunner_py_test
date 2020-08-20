import pypcom
from selenium.webdriver.common.by import By

from src.gui.elements.web_input import WebInput


class SearchBar(pypcom.PageComponent):
    _locator = (By.XPATH, "//div[@class='RNNXgb']")
    input_field = WebInput(By.XPATH, '//div[@class="RNNXgb"]//input')

    def set_search_query(self, query):
        self.input_field.set(query)

    def do_search(self, query):
        self.set_search_query(query)
        self.input_field.press_keys('enter')
        from src.gui.pages.search_result_page import GoogleSearchResultsPage
        return GoogleSearchResultsPage(self.driver)
