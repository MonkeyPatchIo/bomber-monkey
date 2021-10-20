from typing import Tuple, List

from bomber_monkey.features.display.sprite_animation import SpriteAnimation, SpriteAnimationData
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Sprite(Component):
    def __init__(self, path: str, nb_images: int, animation: SpriteAnimation, display_size: Vector,
                 offset: Vector = None, color_tint: Tuple[int, int, int] = None, layer: int = 0,
                 display: bool = True) -> None:
        super().__init__()
        self.display = display
        self.path = path
        self.nb_images = nb_images
        self.animation = animation
        self.display_size = display_size
        self.offset = offset
        self.color_tint = color_tint
        self.layer = layer
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


class SpriteSet(Component):
    def __init__(self, sprites: List[Sprite]):
        super().__init__()
        self.sprites = sprites

