import sys
from enum import IntEnum
import time
from typing import Tuple

import pygame as pg
from pygame.locals import *

import pygameMenu

from pygameMenu.locals import *

from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.display.display_system import DisplaySystem
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.move.move_system import MoveSystem
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.move.speed import Speed
from bomber_monkey.features.physics.collision_system import PlayerWallCollisionSystem
from bomber_monkey.features.physics.friction_system import FrictionSystem
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from python_ecs.ecs import sim, Entity


class AppState(IntEnum):
    APP_START = 1  # No Game launch
    IN_GAME = 2  # Game in-progress
    IN_MENU = 3  # Display menu


class App:
    def __init__(self):
        self.conf = BomberGameConfig()
        self.state = AppState.APP_START
        self.screen = init_pygame(*self.conf.grid_pixel_size)

    def main(self):
        while True:
            if self.state != AppState.IN_GAME:
                self.display_menu()
            else:
                self.run_game()

    def display_menu(self):
        pg.key.set_repeat()
        menu = pygameMenu.Menu(
            self.screen,
            *self.conf.grid_pixel_size,
            font=pygameMenu.fonts.FONT_8BIT,
            title='Bomber Monkey',
            dopause=False
        )
        if self.state > AppState.APP_START:
            menu.add_option('Back to game', self.menu_back_to_game)
        menu.add_option('New game', self.menu_new_game)
        menu.add_option('Exit', PYGAME_MENU_EXIT)

        while self.state != AppState.IN_GAME:
            events = pg.event.get()
            for event in events:
                if event.type == QUIT:
                    exit()
                if self.state > AppState.APP_START and event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                    self.menu_back_to_game()
                    break
            menu.mainloop(events)
            pg.display.flip()

    def menu_back_to_game(self):
        self.state = AppState.IN_GAME

    def menu_new_game(self):
        self.new_game()
        self.menu_back_to_game()

    def menu_background(self):
        self.screen.fill((0, 0, 0))

    def new_game(self):
        board = self.conf.board()
        avatar = self.conf.player(1, 1)

    # create heyboard handlers
    sim.create(Keymap({
        #    https://www.pygame.org/docs/ref/key.html
        pg.K_DOWN: mover(avatar, 0, 1),
        pg.K_UP: mover(avatar, 0, -1),
        pg.K_LEFT: mover(avatar, -1, 0),
        pg.K_RIGHT: mover(avatar, 1, 0),
        pg.K_ESCAPE: lambda e: sim.disable(),
        pg.K_SPACE: bomb_creator(sim, conf, avatar)
    }))

    # init simulation (ECS)
    sim.reset_systems([
        KeyboardSystem(),
        PlayerWallCollisionSystem(board),
        MoveSystem(),
        FrictionSystem(0.995),
        BombExplosionSystem(sim, conf),
        LifetimeSystem(sim),
        BoardDisplaySystem(screen, conf.tile_size),
        DisplaySystem(screen)
    ])

    def run_game(self):
        pg.key.set_repeat(1)
        while self.state == AppState.IN_GAME:
            sim.update()
            pg.display.flip()

    def suspend_game(self):
        self.state = AppState.IN_MENU


def bomb_creator(conf, avatar: Entity):
    def create_bomb(event):
        global last_creation

        now = time.time()
        if now - last_creation > .5:
            last_creation = now
            pos = avatar.get(Position)
            sim.create(
                Position(pos.x, pos.y),
                Speed(),
                Shape(*conf.tile_size),
                Image('resources/bomb.png'),
                Lifetime(conf.bomb_timer_length),
                BombExplosion(3)
            )

    return create_bomb


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


if __name__ == "__main__":
    App().main()
