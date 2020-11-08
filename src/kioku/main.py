"""Kioku Memory Game."""
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from kioku.screens import GameScreen, SettingsScreen  # noqa: F401


Window.size = (700, 900)


class MainScreen(MDScreen):
    """Main screen of the game."""


class KiokuApp(MDApp):
    """Kioku application."""


def main():
    KiokuApp().run()
