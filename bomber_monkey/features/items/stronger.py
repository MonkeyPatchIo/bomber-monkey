from bomber_monkey.features.items.item import consume_item
from bomber_monkey.features.player.stronger import Stronger
from python_ecs.ecs import Component
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System, Simulator


class StrongerItem(Component):
    def __init__(self) -> None:
        super().__init__()


class StrongerItemSystem(System):

    def __init__(self):
        super().__init__([StrongerItem, RigidBody])

    def update(self, sim: Simulator, dt: float, stronger: StrongerItem, body: RigidBody) -> None:
        player_entity = consume_item(sim, stronger, body)
        if player_entity is not None:
            if player_entity.get(Stronger) is None:
                player_entity.attach(Stronger())
