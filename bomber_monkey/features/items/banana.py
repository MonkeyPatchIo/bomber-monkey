from bomber_monkey.features.items.item import consume_item
from bomber_monkey.features.player.player import Player
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
        player_entity = consume_item(sim, banana, body)
        if player_entity is not None:
            player = player_entity.get(Player)
            player.power = min(player.power + 1, 10)
