from bomber_monkey.features.move.speed import Speed
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Entity


class EntityMover(object):
    def __init__(self, avatar: Entity, dir: Vector):
        self.speed = avatar.get(Speed)
        self.dir = dir
        self.is_down = False

    def move(self, event):
        self.is_down = event.type == 2
        if self.is_down:
            self.speed.data += self.dir * .01