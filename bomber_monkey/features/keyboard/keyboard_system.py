import sys

import pygame as pg

from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.states.app_state import AppState
from bomber_monkey.utils.joystick import any_joystick_button
from python_ecs.ecs import System, Simulator


class KeyboardSystem(System):
    def __init__(self):
        super().__init__([Keymap])

    def update(self, sim: Simulator, dt: float, keymap: Keymap) -> None:
        context = sim.context
        if any_joystick_button(first_button=context.conf.JOYSTICK_ESCAPE_BUTTON):
            context.state_manager.change_state(AppState.PAUSE_MENU)

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
