import time
from typing import Callable

from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import Component


class EntityFactory(Component):
    def __init__(self, drop_rate: float, factory: Callable[[RigidBody], None]) -> None:
        super().__init__()
        self.drop_rate = drop_rate
        self.last_drop = 0
        self.factory = factory

    def produce(self, body: RigidBody) -> None:
        now = time.time()
        if now - self.last_drop > self.drop_rate:
            self.last_drop = now
            self.factory(body)

    def __repr__(self):
        return 'EntityFactory({})'.format(self.drop_rate)
