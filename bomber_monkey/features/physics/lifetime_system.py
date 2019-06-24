from bomber_monkey.features.physics.lifetime import Lifetime
from python_ecs.ecs import System

import datetime


class LifetimeSystem(System):
    def __init__(self, sim):
        super().__init__([Lifetime])
        self.sim = sim

    def update(self, ttl: Lifetime) -> None:
        elasped_time = datetime.datetime.now().timestamp() - ttl.start_time
        if elasped_time > ttl.ttl:
            self.sim.get(ttl).destroy()
