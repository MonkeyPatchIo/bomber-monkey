from typing import Dict, List

import pygame
from pygame.surface import Surface

from bomber_monkey.features.display.image import Image
from bomber_monkey.features.display.sprite import Sprite


def _scale(graphic, display_size):
    if display_size is not None:
        return pygame.transform.scale(graphic, display_size.data)
    return graphic


def _change_color(graphic, color_tint):
    if color_tint is None:
        return graphic
    w, h = graphic.get_size()
    for x in range(w):
        for y in range(h):
            color = graphic.get_at((x, y))
            tint_color = pygame.Color(*color_tint)
            tint_color.r = tint_color.r // 5
            tint_color.g = tint_color.g // 5
            tint_color.b = tint_color.b // 5

            if color[3] > 0:
                final_color = color + tint_color
            else:
                final_color = color
            graphic.set_at((x, y), final_color)
    return graphic


class GraphicsCache(object):
    def __init__(self):
        self.images: Dict[Image, Surface] = {}
        self.sprites: Dict[Sprite, List[Surface]] = {}

    def get_image(self, image: Image) -> Surface:
        if image in self.images:
            return self.images[image]

        graphic = pygame.image.load(image.path)
        graphic = _change_color(graphic, image.color_tint)
        graphic = _scale(graphic, image.display_size)

        self.images[image] = graphic
        return graphic

    def get_sprite(self, sprite: Sprite) -> List[Surface]:
        if sprite in self.sprites:
            return self.sprites[sprite]

        source_graphic = pygame.image.load(sprite.path)
        source_width, height = source_graphic.get_size()
        width = source_width / sprite.nb_images
        graphics = [
            source_graphic.subsurface(width * x, 0, width, height)
            for x in range(sprite.nb_images)
        ]
        if sprite.display_size:
            graphics = [
                _change_color(_scale(graphic, sprite.display_size), sprite.color_tint)
                for graphic in graphics
            ]
        self.sprites[sprite] = graphics
        return graphics
