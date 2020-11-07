from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout


class GameScreen(MDScreen):
    """Screen where the game il played."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = GridLayout(cols=3)
        self.add_widget(layout)
