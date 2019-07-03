import sys

import pygame as pg

from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.game_factory import GameFactory
from python_ecs.ecs import System


class KeyboardSystem(System):
    def __init__(self, factory: GameFactory):
        super().__init__([Keymap])
        self.factory = factory

    def update(self, dt: float, keymap: Keymap) -> None:

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                handler = keymap.keymap.get(event.key)
                if handler and handler[0]:
                    handler[0](event)

            if event.type == pg.KEYUP:
                handler = keymap.keymap.get(event.key)
                if handler and handler[1]:
                    handler[1](event)

            if event.type == pg.QUIT:
                sys.exit()
