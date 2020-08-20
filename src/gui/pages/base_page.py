import pypcom


class BasePage(pypcom.Page):
    def __init__(self, driver):
        super().__init__(driver)

    def is_page_opened(self):
        pass
