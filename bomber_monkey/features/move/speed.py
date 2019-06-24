from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Speed(Component):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        super().__init__()
        self.data = Vector.create(x, y)

    def __repr__(self):
        return 'Speed({})'.format(self.data)
