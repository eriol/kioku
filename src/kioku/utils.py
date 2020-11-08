from pathlib import Path
from random import shuffle


class ImageLoader:
    def __init__(self, path):
        self.path = Path(path)
        self.images = []

        self.load()

    def load(self):
        self.images = [f.name for f in self.path.glob("*.jpg")]

    def get_repeated_images(self, times):
        images_to_return = self.images * 2 * times
        shuffle(images_to_return)

        for image in images_to_return:
            yield str(self.path / image)
