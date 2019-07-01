import os

import pygame

from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.states.in_game import GameState
from python_ecs.ecs import System


class BombSoundSystem(System):

    def __init__(self, game_state: GameState):
        super().__init__([Bomb, Lifetime])
        self.game_state = game_state
        path = os.path.abspath('resources/sound/bomb.wav')
        self.effect = pygame.mixer.Sound(path)

    def update(self, dt: float, bomb: Bomb, life: Lifetime) -> None:
        if life.is_ended():
            self.effect.play()
