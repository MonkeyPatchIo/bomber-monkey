from typing import Tuple

import pygame as pg

from bomber_monkey.features.display.image import Image
from bomber_monkey.utils.vector import Vector


class Sprite(Image):
    def __init__(self,
                 path: str,
                 sprite_size: Vector,
                 anim_size: int,
                 size: Vector = None,
                 anim_time: float = None,
                 offset: Vector = None,
                 image_id=-1) -> None:
        super().__init__(path, size, image_id)
        self.sprite_size = sprite_size
        self.anim_size = anim_size
        self.current = 0
        self.anim_time = anim_time
        self.offset = offset

    def change_color(self, image_loader: 'ImageLoader', tint: Tuple[int, int, int]):
        graphic = image_loader[self]
        for _ in range(self.anim_size):
            image = graphic[_]

            w, h = image.get_size()
            for x in range(w):
                for y in range(h):
                    color = image.get_at((x, y))
                    tint_color = pg.Color(*tint)
                    tint_color.r = tint_color.r // 5
                    tint_color.g = tint_color.g // 5
                    tint_color.b = tint_color.b // 5

                    if color[3] > 0:
                        final_color = color + tint_color
                    else:
                        final_color = color
                    image.set_at((x, y), final_color)

    def __repr__(self):
        return 'Sprite({})'.format(self.path)