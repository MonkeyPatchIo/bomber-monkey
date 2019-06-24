from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Shape(Component):
    def __init__(self, dimension: Vector) -> None:
        super().__init__()
        self.data = dimension

    @property
    def width(self):
        return self.data.x

    @property
    def height(self):
        return self.data.y

    def __repr__(self):
        return 'Shape({})'.format(self.data)
