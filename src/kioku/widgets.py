from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.properties import NumericProperty, StringProperty, BooleanProperty


class Card(Button):
    size_hint_x = NumericProperty(0.33)
    text = StringProperty("記憶")
    font_name = "NotoSansCJK-Regular.ttc"
    card_image = StringProperty(None)
    is_discovered = BooleanProperty(False)
    background_down = card_image

    def on_press(self):
        self.text = ""
        if self.card_image:
            self.background_normal = self.card_image

    def reset(self):
        self.text = "記憶"
        self.background_normal = "atlas://data/images/defaulttheme/button"
