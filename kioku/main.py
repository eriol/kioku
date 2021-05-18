"""Kioku Memory Game."""
import shutil
import uuid
from zipfile import ZipFile

from config import settings
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen
from screens import GameScreen  # noqa: F401
from widgets import LevelCoverListItem

LEVELS_EXT = ".zip"


class MainScreen(MDScreen):
    """Main screen of the game."""


class MainToolbar(ThemableBehavior, MDBoxLayout):
    """The main toolbar of the game."""


class KiokuApp(MDApp):
    """Kioku application."""

    dialog = None
    selected_level_path = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[LEVELS_EXT],
        )

    def on_start(self):
        self.load_levels()

    def load_levels(self):
        """Load levels from settings.LEVELS_DIR."""
        for level_path in settings.LEVELS_DIR.iterdir():
            if level_path.is_dir():
                self.root.get_screen("main").ids.levels.add_widget(
                    LevelCoverListItem.from_metadata(level_path)
                )

    def show_alert_delete_level_dialog(self, level_name, level_path):
        if not self.dialog:
            self.dialog = MDDialog(
                title=f"Delete {level_name} level",
                text=f"Are you sure you want to delete {level_name} level?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.close_alert_delete_level_dialog,
                    ),
                    MDFlatButton(
                        text="DELETE",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.close_alert_delete_level,
                    ),
                ],
            )

        self.selected_level_path = level_path
        self.dialog.bind(on_dismiss=self.on_alert_delete_level_dialog_dismiss)
        self.dialog.open()

    def close_alert_delete_level_dialog(self, *args):
        self.dialog.dismiss()

    def on_alert_delete_level_dialog_dismiss(self, *args):
        self.dialog = None
        self.selected_level_path = None

    def close_alert_delete_level(self, *args):
        shutil.rmtree(self.selected_level_path)
        self.reload_levels()
        self.dialog.dismiss()

    def reload_levels(self):
        self.root.get_screen("main").ids.levels.clear_widgets()
        self.load_levels()

    def add_new_level(self):
        self.file_manager.show("/")

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        with ZipFile(path, "r") as zf:
            zf.extractall(settings.LEVELS_DIR / str(uuid.uuid4()))

        self.reload_levels()
        self.exit_manager()


def main():
    KiokuApp().run()


if __name__ == "__main__":
    main()
