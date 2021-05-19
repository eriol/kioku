"""Kioku Memory Game."""
import shutil
import uuid
from pathlib import Path
from random import shuffle
from zipfile import ZipFile

import toml
import xdg
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import BaseListItem, ContainerSupport, IRightBodyTouch
from kivymd.uix.screen import MDScreen

try:
    from android.permissions import Permission, request_permissions

    ON_ANDROID = True
except ImportError:
    ON_ANDROID = False

LEVELS_EXT = ".zip"
# It's OK to keep this simple and support only JPG.
ALLOWED_IMAGES_PATTERN = "*.jpg"
METADATA_FILE_NAME = "metadata.toml"
COLUMNS_NUMBER_KEY = "columns_number"
DEFAULT_COLUMNS_NUMBER = 3
LEVEL_NAME_KEY = "name"
DEFAULT_LEVEL_NAME = "Unknown"


class Settings:
    """Manage settings for kioku."""

    LEVELS_DIR = xdg.xdg_data_home() / "kioku"

    def __init__(self):

        if not self.LEVELS_DIR.exists():
            self.LEVELS_DIR.mkdir(parents=True)


settings = Settings()


class ImageLoader:
    """Load images from the specified path."""

    def __init__(self, path):
        self.path = Path(path)
        self.images = []

        self.load()

    def load(self):
        self.images = [f.name for f in self.path.glob(ALLOWED_IMAGES_PATTERN)]

    def get_repeated_images(self, times):
        images_to_return = self.images * 2 * times
        shuffle(images_to_return)

        for image in images_to_return:
            yield str(self.path / image)


class Card(Button):
    size_hint_x = NumericProperty(0.33)
    text = StringProperty("記憶")
    font_name = "NotoSansCJK-Regular.ttc"
    card_image = StringProperty(None)
    is_discovered = BooleanProperty(False)
    background_down = card_image

    def on_press(self):
        self.text = ""
        if self.card_image:
            self.background_normal = self.card_image

    def reset(self):
        self._fade_out()

    def _fade_out(self):
        anim = Animation(opacity=0)
        anim.bind(on_complete=self._reset)
        anim.start(self)

    def _reset(self, *args):
        self.text = "記憶"
        self.background_normal = "atlas://data/images/defaulttheme/button"

        Clock.schedule_once(self._fade_in)

    def _fade_in(self, *args):
        anim = Animation(opacity=1)
        anim.start(self)


class LevelCoverListItem(ContainerSupport, BaseListItem):
    """A level inside the levels list."""

    name = StringProperty()
    path = StringProperty()
    columns_number = NumericProperty()

    def on_release(self):
        MDApp.get_running_app().root.get_screen("game").level_path = self.path
        MDApp.get_running_app().root.get_screen(
            "game"
        ).columns_number = self.columns_number
        MDApp.get_running_app().root.current = "game"

    @classmethod
    def from_metadata(cls, path):
        """Create a new instance of this class using data inside METADATA_FILE_NAME."""
        with open(path / METADATA_FILE_NAME) as f:
            data = toml.load(f)

        if COLUMNS_NUMBER_KEY not in data:
            data[COLUMNS_NUMBER_KEY] = DEFAULT_COLUMNS_NUMBER

        if LEVEL_NAME_KEY not in data:
            data[LEVEL_NAME_KEY] = DEFAULT_LEVEL_NAME

        data.update({"path": str(path)})

        item = cls(**data)
        item.add_widget(LevelDeleteButton(name=data["name"], path=path))

        return item


class LevelDeleteButton(IRightBodyTouch, MDIconButton):
    """A button to delete a level."""

    def __init__(self, name, path, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.path = str(path)


class GameScreen(MDScreen):
    """Screen where the game is played."""

    level_path = StringProperty()
    columns_number = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_touch_up=self.on_touch_up)
        self.dialog = None

        self.clenup()

    def clenup(self):
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
        """Check if 2 selected cards match."""
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
            Clock.schedule_once(self.on_finish, 1)

    def on_pre_enter(self):
        self.clenup()
        self.load_cards()

    def on_pre_leave(self):
        self.clenup()
        self.clear_widgets()

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

    def on_finish(self, dt):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Congratulations!",
                text=f"You completed the level with {self.errors} errors!",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_press=self.close_dialog,
                    )
                ],
            )

        self.dialog.bind(on_dismiss=self.on_dialog_dismiss)
        self.dialog.open()

    def on_dialog_dismiss(self, *args):
        self.dialog = None

    def close_dialog(self, *args):
        MDApp.get_running_app().root.current = "main"
        self.dialog.dismiss()


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

        if ON_ANDROID:
            request_permissions(
                [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
            )

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
        path = "/storage/emulated/0/" if ON_ANDROID else "/"
        self.file_manager.show(path)

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        with ZipFile(path, "r") as zf:
            zf.extractall(settings.LEVELS_DIR / str(uuid.uuid4()))

        self.reload_levels()
        self.exit_manager()


def run():
    KiokuApp().run()


if __name__ == "__main__":
    run()
