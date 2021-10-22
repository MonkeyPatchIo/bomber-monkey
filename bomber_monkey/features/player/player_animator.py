from typing import Optional
import time
import numpy as np

from bomber_monkey.features.display.sprite import SpriteSet
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.stronger import Stronger
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator

DEFAULT_PLAYER_SIZE = 64

STRONGER_ANIMATION_DURATION = 2.0
STRONGER_SIZE_INCREASE = 20

EPSILON = 0.1


def is_moving_right(body: RigidBody) -> Optional[bool]:
    if body.speed.x > EPSILON:
        return True
    if body.speed.x < -EPSILON:
        return False
    return None


class PlayerAnimatorSystem(System):

    def __init__(self):
        super().__init__([Player, RigidBody, Lifetime, SpriteSet])

    def update(self, sim: Simulator, dt: float, player: Player, body: RigidBody, lifetime: Lifetime,
               sprite_set: SpriteSet) -> None:
        php_sprite = sprite_set.get_sprite("php")
        player_sprite = sprite_set.get_sprite("player")
        rain_sprite = sprite_set.get_sprite("rain")

        dying = lifetime.is_expiring()
        player_sprite.animation.get_anim("dying").enabled = dying

        running = np.linalg.norm(body.speed.data) > EPSILON
        player_sprite.animation.get_anim("running").enabled = running
        player_sprite.animation.get_anim("static").enabled = not running

        moving_right = is_moving_right(body)
        player_sprite.animation.get_anim("moving_right").enabled = moving_right
        rain_sprite.animation.get_anim("moving_right").enabled = moving_right
        php_sprite.animation.get_anim("moving_right").enabled = moving_right

        stronger: Optional[Stronger] = player.entity().get(Stronger)
        if stronger is not None:
            now = time.time()
            if stronger.start_time > now + STRONGER_ANIMATION_DURATION:
                size_increase = STRONGER_SIZE_INCREASE
            else:
                time_to_live = max(stronger.start_time + STRONGER_ANIMATION_DURATION - now, 0)
                size_increase = STRONGER_SIZE_INCREASE * (1 - time_to_live / STRONGER_ANIMATION_DURATION)
            player_sprite.display_size = Vector.create(int(DEFAULT_PLAYER_SIZE + size_increase),
                                                       int(DEFAULT_PLAYER_SIZE + size_increase))
