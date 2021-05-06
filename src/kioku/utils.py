from pathlib import Path
from random import shuffle

# It's OK to keep this simple and support only JPG.
ALLOWED_IMAGES_PATTERN = "*.jpg"


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
