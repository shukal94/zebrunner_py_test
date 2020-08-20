import pytest

from src.common.context import Context, Parameter
from src.gui.pages.start_page import GoogleStartPage
from test.gui_test import driver_pool


@pytest.mark.smoke
class TestGoogleBase:

    SEARCH_QUERY = 'lala'

    def setup(self):
        self.driver = driver_pool.create_driver()
        self.driver.get(Context.get_gui_parameter(Parameter.BASE_URL))

    def teardown(self):
        self.driver.quit()

    def test_start_page_is_opened(self):
        google_start_page = GoogleStartPage(self.driver)
        assert google_start_page.is_page_opened(), 'Start page was not opened!'

    def test_google_search_from_start(self):
        google_start_page = GoogleStartPage(self.driver)
        assert google_start_page.is_page_opened(), 'Start page was not opened!'
        search_bar = google_start_page.search_bar
        assert search_bar.is_present(), 'Search bar is not present!'
        search_results_page = search_bar.do_search(self.SEARCH_QUERY)
        assert search_results_page.is_page_opened(), 'Search results page was not opened!'
