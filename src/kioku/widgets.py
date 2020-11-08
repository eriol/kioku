from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.button import Button


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
        self._fade_out()

    def _fade_out(self):
        anim = Animation(opacity=0)
        anim.bind(on_complete=self._reset)
        anim.start(self)

    def _reset(self, *args):
        self.text = "記憶"
        self.background_normal = "atlas://data/images/defaulttheme/button"

        Clock.schedule_once(self._fade_in)

    def _fade_in(self, *args):
        anim = Animation(opacity=1)
        anim.start(self)
