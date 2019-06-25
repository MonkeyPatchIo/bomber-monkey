from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Entity


class EntityMover(object):
    def __init__(self, avatar: Entity, dir: Vector):
        self.body: RigidBody = avatar.get(RigidBody)
        self.dir = dir

    def callbacks(self):
        return self.on_key_down(), self.on_key_up()

    def on_key_down(self):
        def move(event):
            self.body.accel += self.dir

        return move

    def on_key_up(self):
        def move(event):
            self.body.accel *= 0

        return move
