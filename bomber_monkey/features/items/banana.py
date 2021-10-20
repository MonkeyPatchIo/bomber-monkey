from bomber_monkey.features.items.item import consume_item
from python_ecs.ecs import Component
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System, Simulator


class Banana(Component):
    def __init__(self) -> None:
        super().__init__()


class BananaSystem(System):

    def __init__(self):
        super().__init__([Banana, RigidBody])

    def update(self, sim: Simulator, dt: float, banana: Banana, body: RigidBody) -> None:
        player = consume_item(sim, banana, body)
        if player is not None:
            player.power = min(player.power + 1, 10)
