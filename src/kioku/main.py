"""Kioku Memory Game."""
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from kioku.screens import GameScreen  # noqa: F401


class MainScreen(MDScreen):
    """Main screen of the game."""


class KiokuApp(MDApp):
    """Kioku application."""


def main():
    KiokuApp().run()
