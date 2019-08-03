from typing import Tuple

from bomber_monkey.features.display.sprite_animation import SpriteAnimation, SpriteAnimationData
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Sprite(Component):
    def __init__(self, path: str, nb_images: int, animation: SpriteAnimation, display_size: Vector,
                 offset: Vector = None, color_tint: Tuple[int, int, int] = None) -> None:
        super().__init__()
        self.path = path
        self.nb_images = nb_images
        self.animation = animation
        self.display_size = display_size
        self.offset = offset
        self.color_tint = color_tint
        self.animation_data = SpriteAnimationData(nb_images)

    def __eq__(self, other):
        if isinstance(other, Sprite):
            return self.path == other.path and self.display_size == other.display_size\
                   and self.color_tint == other.color_tint
        return False

    def __hash__(self):
        return hash((self.path, self.display_size, self.color_tint))

    def __repr__(self):
        return 'Sprite({})'.format(self.path)

