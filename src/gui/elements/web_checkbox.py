from src.gui.elements.web_clickable import WebClickable


class WebCheckbox(WebClickable):

    def __init__(self, by, value):
        self.by = by
        self.value = value
        super().__init__(by, value)

    def is_selected(self):
        return self.get_attribute('value').lower() in ['true', 'on']
