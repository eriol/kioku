from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen

from .utils import ImageLoader
from .widgets import Card


class GameScreen(MDScreen):
    """Screen where the game is played."""

    level_path = StringProperty()
    columns_number = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_touch_up=self.on_touch_up)

        self.cards = []

    def on_touch_up(self, touch, *args):
        if args:
            for k in args[0].ud:
                if isinstance(k, Card) and not k.is_discovered:
                    self.cards.append(k)

            self.check_cards()

    def check_cards(self):
        if len(self.cards) == 2:
            card1, card2 = self.cards
            if card1.card_image != card2.card_image:
                card1.reset()
                card2.reset()
            else:
                card1.is_discovered = True
                card2.is_discovered = True
            self.cards = []

    def on_pre_enter(self):
        self.load_cards()

    def load_cards(self):
        loader = ImageLoader(self.level_path)

        self.layout = GridLayout(cols=self.columns_number)
        self.add_widget(self.layout)
        for image in loader.get_repeated_images(times=2):
            self.layout.add_widget(Card(card_image=image))


class SettingsScreen(MDScreen):
    """Screen for settings."""
