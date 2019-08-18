from bomber_monkey.features.lifetime.lifetime import Lifetime
from python_ecs.ecs import System, Simulator


class LifetimeSystem(System):
    def __init__(self):
        super().__init__([Lifetime])

    def update(self, sim: Simulator, dt: float, lifetime: Lifetime) -> None:
        if lifetime.is_ended():
            lifetime.entity().destroy()
        # NB: we update the life time AFTER checking for the end of life. Because this system is the last system to
        # apply, we must let a chance for the other systems to detect the end of life in the next loop
        lifetime.add_to_life(dt)
