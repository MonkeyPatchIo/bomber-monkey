from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Position(Component):
    def __init__(self, pos: Vector) -> None:
        super().__init__()
        self.data = pos

    def __repr__(self):
        return 'Position({})'.format(self.data)
