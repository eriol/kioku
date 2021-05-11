"""Kioku Memory Game."""
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
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

    dialog = None

    def on_start(self):
        self.load_levels()

    def load_levels(self):
        """Load levels from settings.LEVELS_DIR."""
        for level_path in settings.LEVELS_DIR.iterdir():
            if level_path.is_dir():
                self.root.get_screen("main").ids.levels.add_widget(
                    LevelCoverListItem.from_metadata(level_path)
                )

    def show_alert_delete_level_dialog(self, level_name):
        if not self.dialog:
            self.dialog = MDDialog(
                text=f"Delete {level_name} level?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.close_alert_delete_level_dialog,
                    ),
                    MDFlatButton(
                        text="DELETE", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.bind(on_dismiss=self.on_alert_delete_level_dialog_dismiss)
        self.dialog.open()

    def close_alert_delete_level_dialog(self, *args):
        self.dialog.dismiss()

    def on_alert_delete_level_dialog_dismiss(self, *args):
        self.dialog = None


def main():
    KiokuApp().run()
