from typing import Dict

import pygame
from pygame.surface import Surface

from bomber_monkey.features.display.image import Image


class ImageLoader(object):
    def __init__(self):
        self.graphics: Dict[Image, Surface] = {}

    def __getitem__(self, image):
        graphic = self.graphics.get(image, None)
        if graphic is None:
            graphic = pygame.image.load(image.path)
            if image.size:
                graphic = pygame.transform.scale(graphic, image.size.data)
            self.graphics[image] = graphic
        return graphic