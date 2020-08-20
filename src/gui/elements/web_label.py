from src.gui.elements.web_base_element import WebBaseElement


class WebLabel(WebBaseElement):

    def __init__(self, by, value):
        self.by = by
        self.value = value
        super().__init__(by, value)
