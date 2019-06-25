from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Position(Component):
    def __init__(self, pos: Vector = None) -> None:
        super().__init__()
        self.pos = pos or Vector.create()

    def __repr__(self):
        return 'Position({})'.format(self.pos)


class Speed(Component):
    def __init__(self, speed: Vector = None) -> None:
        super().__init__()
        self.speed = speed or Vector.create()

    def __repr__(self):
        return 'Speed({})'.format(self.speed)


class Accel(Component):
    def __init__(self, accel: Vector = None) -> None:
        super().__init__()
        self.accel = accel or Vector.create()

    def __repr__(self):
        return 'Accel({})'.format(self.accel)
