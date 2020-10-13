"""Kioku Memory Game."""
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class MainScreen(MDScreen):
    """Main screen of the game."""


class GameScreen(MDScreen):
    """Screen where the game il played."""


class KiokuApp(MDApp):
    """Kioku application."""


if __name__ == "__main__":
    KiokuApp().run()
