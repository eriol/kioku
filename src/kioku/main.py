from kivy.app import App
from kivy.uix.widget import Widget
import kivy

kivy.require("1.11.0")


class CardWidget(Widget):
    """A flipping card."""


class KiokuApp(App):
    def build(self):
        return CardWidget()


if __name__ == "__main__":
    KiokuApp().run()
