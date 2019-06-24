import sys
from typing import Tuple

import pygame as pg
from pygame.locals import *

import pygameMenu

from pygameMenu.locals import *

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.display.display_system import DisplaySystem
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.move.move_system import MoveSystem
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.move.speed import Speed
from bomber_monkey.features.physics.friction_system import FrictionSystem
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import sim, Entity


class BomberGameConfig(object):
    def __init__(self):
        self.tile_size = (64, 64)
        self.grid_size = (25, 15)

    @property
    def grid_pixel_size(self) -> Tuple[int, int]:
        return self.tile_size[0] * self.grid_size[0], self.tile_size[1] * self.grid_size[1]


def main():
    conf = BomberGameConfig()

    # init pygame
    screen = init_pygame(*conf.grid_pixel_size)

    menu = pygameMenu.Menu(screen, 1400, 900, font=pygameMenu.fonts.FONT_8BIT, title='Bomber Monkey', bgfun=lambda: menu_background(screen))
    menu.add_option('New game', lambda: new_name(screen, conf))
    menu.add_option('Return', lambda: run_game(sim))
    menu.add_option('Exit', PYGAME_MENU_EXIT)
    menu.enable()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        menu.mainloop(events)
        pg.display.flip()


def menu_background(screen):
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    screen.fill((0, 0, 0))


def new_name(screen, conf):
    # init simulation (ECS)
    sim.reset_systems([
        KeyboardSystem(),
        MoveSystem(),
        FrictionSystem(0.995),
        BoardDisplaySystem(screen, conf.tile_size),
        DisplaySystem(screen)
    ])
    # create board
    board = sim.create(Board(tile_size=conf.tile_size, grid_size=conf.grid_size))

    # create avatar
    avatar = sim.create(
        Position(50, 50),
        Speed(),
        Shape(*conf.tile_size),
        Image('resources/bomb.png')
    )
    # create heyboard handlers
    sim.create(Keymap({
        #    https://www.pygame.org/docs/ref/key.html
        pg.K_DOWN: mover(avatar, 0, 1),
        pg.K_UP: mover(avatar, 0, -1),
        pg.K_LEFT: mover(avatar, -1, 0),
        pg.K_RIGHT: mover(avatar, 1, 0),
        pg.K_ESCAPE: lambda e: sim.disable()
    }))

    run_game(sim)


def mover(obj: Entity, dx: int, dy: int):
    def move(event):
        if event.type == pg.KEYDOWN:
            speed = obj.get(Speed)
            speed.x += dx * .01
            speed.y += dy * .01

    return move


def init_pygame(screen_width, screen_height):
    pg.init()
    pg.key.set_repeat(1)
    # load and set the logo
    logo = pg.image.load("resources/bomb.png")
    pg.display.set_icon(logo)
    pg.display.set_caption('my game')
    screen = pg.display.set_mode((screen_width, screen_height))
    return screen


def run_game(sim):
    sim.enable()
    while sim.is_enabled():
        sim.update()
        pg.display.flip()


if __name__ == "__main__":
    main()
