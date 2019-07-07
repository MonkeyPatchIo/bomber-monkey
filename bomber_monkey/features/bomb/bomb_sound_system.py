import os

import pygame

from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.lifetime.lifetime import Lifetime
from python_ecs.ecs import System, Simulator


class BombSoundSystem(System):

    def __init__(self):
        super().__init__([Bomb, Lifetime])
        path = os.path.abspath('resources/sound/bomb.wav')
        self.effect = pygame.mixer.Sound(path)

    def update(self, sim: Simulator, dt: float, bomb: Bomb, life: Lifetime) -> None:
        if life.is_ended():
            self.effect.play()
