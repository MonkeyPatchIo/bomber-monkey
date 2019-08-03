from typing import Tuple

from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Image(Component):
    def __init__(self, path: str, display_size: Vector = None, color_tint: Tuple[int, int, int] = None) -> None:
        super().__init__()
        self.path = path
        self.display_size = display_size
        self.color_tint = color_tint

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.path == other.path and self.display_size == other.display_size\
                   and self.color_tint == other.color_tint
        return False

    def __hash__(self):
        return hash((self.path, self.display_size, self.color_tint))

    def __repr__(self):
        return 'Image({})'.format(self.path)


