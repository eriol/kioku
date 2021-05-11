"""Kioku Memory Game."""
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

from .config import settings
from .screens import GameScreen, SettingsScreen  # noqa: F401
from .widgets import LevelCoverListItem

Window.size = (700, 900)


class MainScreen(MDScreen):
    """Main screen of the game."""


class MainToolbar(ThemableBehavior, MDBoxLayout):
    """The main toolbar of the game."""


class KiokuApp(MDApp):
    """Kioku application."""

    def on_start(self):
        self.load_levels()

    def load_levels(self):
        """Loads levels from settings.LEVELS_DIR."""
        for level_path in settings.LEVELS_DIR.iterdir():
            if level_path.is_dir():
                self.root.get_screen("main").ids.levels.add_widget(
                    LevelCoverListItem.from_metadata(level_path)
                )


def main():
    KiokuApp().run()
