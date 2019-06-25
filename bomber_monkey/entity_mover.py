from bomber_monkey.features.move.move import Speed, Accel
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Entity


class EntityMover(object):
    def __init__(self, avatar: Entity, dir: Vector):
        self.accel = avatar.get(Accel)  # type: Accel
        self.dir = dir

    def callbacks(self):
        return self.on_key_down(), self.on_key_up()

    def on_key_down(self):
        def move(event):
            self.accel.accel += self.dir

        return move

    def on_key_up(self):
        def move(event):
            self.accel.accel *= 0

        return move
