import sys

import pygame as pg

from bomber_monkey.features.keyboard.keymap import Keymap
from python_ecs.ecs import System


class KeyboardSystem(System):
    def __init__(self):
        super().__init__([Keymap])

    def update(self, keymap: Keymap) -> None:
        for event in pg.event.get():

            if event.type in (pg.KEYDOWN, pg.KEYUP):
                handler = keymap.keymap.get(event.key)
                if handler:
                    handler(event)

            if event.type == pg.QUIT:
                sys.exit()
