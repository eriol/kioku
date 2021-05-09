import xdg


class Settings:
    """Manage settings for kioku."""

    LEVELS_DIR = xdg.xdg_data_home() / "kioku"

    def __init__(self):

        if not self.LEVELS_DIR.exists():
            self.LEVELS_DIR.mkdir(parents=True)


settings = Settings()
