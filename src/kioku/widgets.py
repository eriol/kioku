import toml
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import BaseListItem, ContainerSupport, IRightBodyTouch

METADATA_FILE_NAME = "metadata.toml"
COLUMNS_NUMBER_KEY = "columns_number"
DEFAULT_COLUMNS_NUMBER = 3


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
    """A level inside the level list."""

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
