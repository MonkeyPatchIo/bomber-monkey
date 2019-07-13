from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class RigidBody(Component):
    def __init__(self,
                 mass: float = 1,
                 pos: Vector = None,
                 speed: Vector = None,
                 accel: Vector = None,
                 shape: Shape = None,
                 ) -> None:
        super().__init__()
        self.mass = mass
        self.pos = pos or Vector.create()
        self.speed = speed or Vector.create()
        self.accel = accel or Vector.create()
        self.shape = shape

    def __repr__(self):
        return 'RigidBody({})'.format(self.mass)
