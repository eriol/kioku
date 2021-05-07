"""Kioku Memory Game."""
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

from .screens import GameScreen, SettingsScreen  # noqa: F401

Window.size = (700, 900)


class MainScreen(MDScreen):
    """Main screen of the game."""


class MainToolbar(ThemableBehavior, MDBoxLayout):
    """The main toolbar of the game."""


class KiokuApp(MDApp):
    """Kioku application."""


def main():
    KiokuApp().run()
