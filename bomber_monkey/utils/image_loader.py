from typing import Dict, List, Union

import pygame
from pygame.surface import Surface

from bomber_monkey.features.display.image import Image
from bomber_monkey.features.display.sprite import Sprite


class ImageLoader(object):
    def __init__(self):
        self.graphics: Dict[Image, Union[Surface, List[Surface]]] = {}

    def __getitem__(self, image: Image):
        if image not in self.graphics:
            graphic = pygame.image.load(image.path)

            if isinstance(image, Sprite):
                sprite: Sprite = image
                w, h = sprite.sprite_size.data
                images = [graphic.subsurface(w * x, 0, w, h) for x in range(sprite.anim_size)]
                if sprite.size:
                    images = [pygame.transform.scale(img, sprite.size.data) for img in images]
                self.graphics[sprite] = images
            else:
                if image.size:
                    graphic = pygame.transform.scale(graphic, image.size.data)
                self.graphics[image] = graphic
        return self.graphics[image]
