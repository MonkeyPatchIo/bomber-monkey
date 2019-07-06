from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.spawner.spawner import Spawner
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class PlayerController(Component):
    @staticmethod
    def from_keyboard(player_seed: float, left_key, right_key, up_key, down_key, action_key):
        return PlayerController(player_seed, left_key, right_key, up_key, down_key, action_key)

    @staticmethod
    def from_joystick(player_seed: float, joystick, axis_x, axis_y):
        return PlayerController(player_seed, None, None, None, None, None, joystick, axis_x, axis_y)

    def __init__(self, player_speed: float,
                 left_key, right_key, up_key, down_key, action_key,
                 joystick=None,
                 axis_x=False,
                 axis_y=False):
        super().__init__()
        self.joystick = joystick
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.actions = {
            left_key: self.left_action,
            right_key: self.right_action,
            up_key: self.up_action,
            down_key: self.down_action,
            action_key: self.special_action,
        }

        self.player_speed = player_speed

    def left_action(self, body: RigidBody):
        body.speed += Vector.create(-self.player_speed, 0)

    def right_action(self, body: RigidBody):
        body.speed += Vector.create(self.player_speed, 0)

    def up_action(self, body: RigidBody):
        body.speed += Vector.create(0, -self.player_speed)

    def down_action(self, body: RigidBody):
        body.speed += Vector.create(0, self.player_speed)

    def special_action(self, body: RigidBody):
        dropper: Spawner = body.entity().get(Spawner)
        dropper.produce(body)
