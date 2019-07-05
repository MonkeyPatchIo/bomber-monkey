from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Image(Component):
    def __init__(self, path: str, size: Vector = None, image_id=-1) -> None:
        super().__init__()
        self.image_id = image_id
        self.path = path
        self.size = size

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.path == other.path and self.size == other.size and self.image_id == other.image_id
        return False

    def __hash__(self):
        return hash((self.path, self.size, self.image_id))

    def __repr__(self):
        return 'Image({})'.format(self.path)


