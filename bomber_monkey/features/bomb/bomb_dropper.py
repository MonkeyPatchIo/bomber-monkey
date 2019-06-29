import time

from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import Component


class BombDropper(Component):
    def __init__(self, drop_rate: float) -> None:
        super().__init__()
        self.drop_rate = drop_rate
        self.last_drop = 0

    def drop(self, game_state, body: RigidBody) -> None:
        now = time.time()
        if now - self.last_drop > self.drop_rate:
            self.last_drop = now
            game_state.create_bomb(body)

    def __repr__(self):
        return 'BombDropper({})'.format(self.drop_rate)
