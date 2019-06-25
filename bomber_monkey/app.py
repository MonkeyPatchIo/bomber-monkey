from enum import IntEnum
import time

import pygame as pg
from pygame.locals import *

import pygameMenu

from pygameMenu.locals import *

from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.entity_mover import EntityMover
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.bomb.player_killer_system import PlayerKillerSystem
from bomber_monkey.features.display.display_system import DisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.physics.collision_system import WallCollisionSystem
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import sim, Entity


class AppState(IntEnum):
    APP_START = 1  # No Game launch
    IN_GAME = 2  # Game in-progress
    IN_MENU = 3  # Display menu


class App:
    def __init__(self):
        self.conf = BomberGameConfig()
        self.state = AppState.APP_START
        self.screen = init_pygame(*self.conf.pixel_size.data)

    def main(self):
        while True:
            if self.state != AppState.IN_GAME:
                self.display_menu()
            else:
                self.run_game()

    def display_menu(self):
        menu = pygameMenu.Menu(
            self.screen,
            *self.conf.pixel_size.data,
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

    def new_game(self):
        board = self.conf.create_board()

        avatar = self.conf.create_player(Vector.create(1, 1))
        avatar2 = self.conf.create_player(Vector.create(self.conf.board.width - 2, self.conf.board.height - 2))

        accel = .25

        # create heyboard handlers
        sim.create(Keymap({
            #    https://www.pygame.org/docs/ref/key.html
            pg.K_DOWN: EntityMover(avatar2, Vector.create(0, accel)).callbacks(),
            pg.K_UP: EntityMover(avatar2, Vector.create(0, -accel)).callbacks(),
            pg.K_LEFT: EntityMover(avatar2, Vector.create(-accel, 0)).callbacks(),
            pg.K_RIGHT: EntityMover(avatar2, Vector.create(accel, 0)).callbacks(),
            pg.K_RETURN: (
                bomb_creator(self.conf, avatar2),
                None
            ),

            pg.K_s: EntityMover(avatar, Vector.create(0, accel)).callbacks(),
            pg.K_z: EntityMover(avatar, Vector.create(0, -accel)).callbacks(),
            pg.K_q: EntityMover(avatar, Vector.create(-accel, 0)).callbacks(),
            pg.K_d: EntityMover(avatar, Vector.create(accel, 0)).callbacks(),
            pg.K_SPACE: (
                bomb_creator(self.conf, avatar),
                None
            ),

            pg.K_ESCAPE: (None, lambda e: self.suspend_game()),
        }))

        # init simulation (ECS)
        sim.reset_systems([
            KeyboardSystem(),

            WallCollisionSystem(board),
            PhysicSystem(.995),
            PlayerKillerSystem(self.conf),

            BombExplosionSystem(self.conf),
            LifetimeSystem(),

            BoardDisplaySystem(self.conf.image_loader, self.screen, self.conf.tile_size),
            DisplaySystem(self.conf.image_loader, self.screen)
        ])

    def run_game(self):
        clock = pg.time.Clock()

        while self.state == AppState.IN_GAME:
            sim.update()
            pg.display.flip()
            clock.tick(60)

    def suspend_game(self):
        self.state = AppState.IN_MENU


last_creation = time.time()


def bomb_creator(conf: BomberGameConfig, avatar: Entity):
    def create(event):
        conf.create_bomb(avatar)

    return create


def init_pygame(screen_width, screen_height):
    pg.init()
    # load and set the logo
    logo = pg.image.load("resources/bomb.png")
    pg.display.set_icon(logo)
    pg.display.set_caption('my game')
    screen = pg.display.set_mode((screen_width, screen_height))
    return screen


if __name__ == "__main__":
    App().main()
