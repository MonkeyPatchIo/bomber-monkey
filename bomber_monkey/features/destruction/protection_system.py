from bomber_monkey.features.destruction.destruction import Protection
from python_ecs.ecs import System, Simulator


class ProtectionSystem(System):

    def __init__(self):
        super().__init__([Protection])

    def update(self, sim: Simulator, dt: float, protection: Protection) -> None:
        if protection.remaining > 0:
            protection.remaining -= dt
        else:
            protection.remaining = 0
