from bomber_monkey.features.destruction.destruction import Protection
from bomber_monkey.features.display.sprite import SpriteSet
from bomber_monkey.features.player.player import Player
from python_ecs.ecs import System, Simulator


class ProtectionSystem(System):

    def __init__(self):
        super().__init__([Protection])

    def update(self, sim: Simulator, dt: float, protection: Protection) -> None:
        if protection.remaining > 0:
            protection.remaining -= dt
            if protection.remaining < 0:
                protection.remaining = 0
                entity = protection.entity()
                if entity.get(Player):
                    sprite_set: SpriteSet = entity.get(SpriteSet)
                    sprite_set.sprites[0].display = False
                    sprite_set.sprites[2].display = False
