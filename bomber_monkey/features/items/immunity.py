from bomber_monkey.features.destruction.destruction import Protection
from bomber_monkey.features.display.sprite import SpriteSet
from bomber_monkey.features.items.item import consume_item
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import Component
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System, Simulator


class ImmunityItem(Component):
    def __init__(self) -> None:
        super().__init__()


class ImmunityItemSystem(System):

    def __init__(self, conf: GameConfig):
        super().__init__([ImmunityItem, RigidBody])
        self.conf = conf

    def update(self, sim: Simulator, dt: float, immunity: ImmunityItem, body: RigidBody) -> None:
        player_entity = consume_item(sim, immunity, body)
        if player_entity is not None:
            protection: Protection = player_entity.get(Protection)
            protection.remaining = self.conf.immunity_duration
            sprite_set: SpriteSet = player_entity.get(SpriteSet)
            sprite_set.sprites[0].display = True
            sprite_set.sprites[2].display = True
