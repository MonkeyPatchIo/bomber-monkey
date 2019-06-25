from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System


class MoveSystem(System):
    def __init__(self):
        super().__init__([RigidBody])

    def update(self, body: RigidBody) -> None:
        body.speed += body.accel
        body.pos += body.speed
