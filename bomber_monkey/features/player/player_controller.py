from typing import Callable, Any, Dict

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.systems.entity_factory import EntityBuilder
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class PlayerController(Component):
    @staticmethod
    def from_keyboard(left_key, right_key, up_key, down_key, action_key):
        return PlayerController(left_key, right_key, up_key, down_key, action_key)

    @staticmethod
    def from_joystick(joystick):
        return PlayerController(None, None, None, None, None, joystick)

    def __init__(self, left_key, right_key, up_key, down_key, action_key, joystick=None):
        super().__init__()
        self.joystick = joystick
        self.actions = {
            left_key: self.left_action,
            right_key: self.right_action,
            up_key: self.up_action,
            down_key: self.down_action,
            action_key: self.special_action,
        }

        self.accel = 1

    def left_action(self, body: RigidBody):
        body.speed += Vector.create(-self.accel, 0)

    def right_action(self, body: RigidBody):
        body.speed += Vector.create(self.accel, 0)

    def up_action(self, body: RigidBody):
        body.speed += Vector.create(0, -self.accel)

    def down_action(self, body: RigidBody):
        body.speed += Vector.create(0, self.accel)

    def special_action(self, body: RigidBody):
        dropper: EntityBuilder = body.entity().get(EntityBuilder)
        dropper.produce(body)
