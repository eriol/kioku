from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

from kivymd.uix.screen import MDScreen

from .widgets import Card


class GameScreen(MDScreen):
    """Screen where the game is played."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_touch_up=self.on_touch_up)

        self.cards = []

        self.layout = GridLayout(cols=3)
        self.add_widget(self.layout)

        self.load_cards()

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

    def load_cards(self):
        pass
