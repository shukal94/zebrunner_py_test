from src.gui.elements.web_clickable import WebClickable


class WebLink(WebClickable):

    def __init__(self, by, value):
        self.by = by
        self.value = value
        super().__init__(by, value)
