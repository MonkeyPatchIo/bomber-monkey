from bomber_monkey.features.lifetime.lifetime import Lifetime
from python_ecs.ecs import System, sim

import datetime


class LifetimeSystem(System):
    def __init__(self):
        super().__init__([Lifetime])

    def update(self, lifetime: Lifetime) -> None:
        now = datetime.datetime.now().timestamp()
        if now > lifetime.dead_time:
            sim.get(lifetime.eid).destroy()
