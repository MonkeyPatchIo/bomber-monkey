from bomber_monkey.features.items.item import consume_item
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import Component
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System, Simulator


class SpeedUpItem(Component):
    def __init__(self) -> None:
        super().__init__()


class SpeedUpItemSystem(System):

    def __init__(self, conf: GameConfig):
        super().__init__([SpeedUpItem, RigidBody])
        self.conf = conf

    def update(self, sim: Simulator, dt: float, speedup: SpeedUpItem, body: RigidBody) -> None:
        player_entity = consume_item(sim, speedup, body)
        if player_entity is not None:
            player_body = player_entity.get(RigidBody)
            max_speed = player_body.max_speed if player_body.max_speed is not None else self.conf.player_max_speed
            player_body.max_speed = max_speed * self.conf.speed_up
