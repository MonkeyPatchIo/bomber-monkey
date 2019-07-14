from bomber_monkey.features.lifetime.lifetime import Lifetime
from python_ecs.ecs import System, Simulator


class LifetimeSystem(System):
    def __init__(self):
        super().__init__([Lifetime])

    def update(self, sim: Simulator, dt: float, lifetime: Lifetime) -> None:
        if lifetime.is_ended():
            lifetime.entity().destroy()
