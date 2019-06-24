import sys

import pygame as pg

from bomber_monkey.features.keyboard.keymap import Keymap
from python_ecs.ecs import System


class KeyboardSystem(System):
    def __init__(self):
        super().__init__([Keymap])

    def update(self, keymap: Keymap) -> None:
        for event in pg.event.get():
            try:
                if event.type == pg.KEYDOWN:
                    print('DOWN: ' + str(event))
                    handler = keymap.keymap.get(event.key)
                    handler[0](event)
            except Exception as e:
                pass

            try:
                if event.type == pg.KEYUP:
                    print('UP: ' + str(event))

                    handler = keymap.keymap.get(event.key)
                    handler[1](event)
            except Exception as e:
                pass

            if event.type == pg.QUIT:
                sys.exit()
