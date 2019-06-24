from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Position(Component):
    def __init__(self, pos: Vector = None) -> None:
        super().__init__()
        self.data = pos or Vector.create()

    def __repr__(self):
        return 'Position({})'.format(self.data)


class Speed(Component):
    def __init__(self, speed: Vector = None) -> None:
        super().__init__()
        self.data = speed or Vector.create()

    def __repr__(self):
        return 'Speed({})'.format(self.data)


class Accel(Component):
    def __init__(self, accel: Vector = None) -> None:
        super().__init__()
        self.data = accel or Vector.create()

    def __repr__(self):
        return 'Accel({})'.format(self.data)
