from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen

from .utils import ImageLoader
from .widgets import Card


class GameScreen(MDScreen):
    """Screen where the game is played."""

    level_path = StringProperty()
    columns_number = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_touch_up=self.on_touch_up)

        self.cards_deck = []
        self.cards_pair = []
        self.errors = 0

    def on_touch_up(self, touch, *args):
        if args:
            for k in args[0].ud:
                if isinstance(k, Card) and not k.is_discovered:
                    self.cards_pair.append(k)

            self.check_cards_pair()

    def check_cards_pair(self):
        if len(self.cards_pair) == 2:
            card1, card2 = self.cards_pair
            if card1.card_image != card2.card_image:
                card1.reset()
                card2.reset()
                self.errors += 1
            else:
                card1.is_discovered = True
                card2.is_discovered = True
            self.cards_pair = []

        if self.check_game_finish():
            pass

    def on_pre_enter(self):
        self.load_cards()

    def load_cards(self):
        """Load cards from the path level specified."""
        loader = ImageLoader(self.level_path)

        self.cards_deck = GridLayout(cols=self.columns_number)
        self.add_widget(self.cards_deck)
        for image in loader.get_repeated_images(times=2):
            self.cards_deck.add_widget(Card(card_image=image))

    def check_game_finish(self):
        """Check if the game is finished."""
        if hasattr(self.cards_deck, "children"):
            return all([card.is_discovered for card in self.cards_deck.children])

        return False


class SettingsScreen(MDScreen):
    """Screen for settings."""
