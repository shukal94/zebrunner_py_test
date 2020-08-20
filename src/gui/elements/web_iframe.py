from src.gui.elements.web_base_element import WebBaseElement


class WebIframe(WebBaseElement):

    def __init__(self, by, value):
        self.by = by
        self.value = value
        super().__init__(by, value)

    def switch(self):
        iframe = self.get_element()
        self.driver.switch_to.frame(iframe)
