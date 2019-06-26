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
from bomber_monkey.features.display.display_system import DisplaySystem, SpriteDisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.physics.collision_system import PlayerCollisionSystem
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_state import GameState
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import sim, Entity


class AppState(IntEnum):
    MAIN_MENU = 1  # No Game launch
    IN_GAME = 2  # Game in-progress
    PAUSE_MENU = 3  # Display menu
    STAGE_END = 4  # End of game, display score


class App:
    def __init__(self):
        self.conf = BomberGameConfig()
        self.app_state = AppState.MAIN_MENU
        self.screen = init_pygame(*self.conf.pixel_size.data)

    def main(self):
        while True:
            if self.app_state == AppState.MAIN_MENU:
                run_main_menu(self)
            elif self.app_state == AppState.IN_GAME:
                run_game(self)
            elif self.app_state == AppState.PAUSE_MENU:
                run_pause_menu(self)
            elif self.app_state == AppState.STAGE_END:
                run_end_game(self)
            else:
                raise RuntimeError

    def pause_game(self):
        self.app_state = AppState.PAUSE_MENU

    def back_to_game(self):
        self.app_state = AppState.IN_GAME

    def new_game(self):
        self.scores = [0] * 2
        self.new_round()

    def new_round(self):
        self.app_state = AppState.IN_GAME
        sim.reset()
        self.game_state = GameState(self.conf)

        board = self.game_state.create_board()

        avatar = self.game_state.create_player(Vector.create(1, 1))
        avatar2 = self.game_state.create_player(Vector.create(self.game_state.board.width - 2, self.game_state.board.height - 2))

        accel = 1

        # create heyboard handlers
        sim.create(Keymap({
            #    https://www.pygame.org/docs/ref/key.html
            pg.K_DOWN: EntityMover(avatar2, Vector.create(0, accel)).callbacks(),
            pg.K_UP: EntityMover(avatar2, Vector.create(0, -accel)).callbacks(),
            pg.K_LEFT: EntityMover(avatar2, Vector.create(-accel, 0)).callbacks(),
            pg.K_RIGHT: EntityMover(avatar2, Vector.create(accel, 0)).callbacks(),
            pg.K_RETURN: (
                bomb_creator(self.game_state, avatar2),
                None
            ),

            pg.K_s: EntityMover(avatar, Vector.create(0, accel)).callbacks(),
            pg.K_z: EntityMover(avatar, Vector.create(0, -accel)).callbacks(),
            pg.K_q: EntityMover(avatar, Vector.create(-accel, 0)).callbacks(),
            pg.K_d: EntityMover(avatar, Vector.create(accel, 0)).callbacks(),
            pg.K_SPACE: (
                bomb_creator(self.game_state, avatar),
                None
            ),

            pg.K_ESCAPE: (None, lambda e: self.pause_game()),
        }))

        # init simulation (ECS)
        sim.reset_systems([
            KeyboardSystem(),

            PlayerCollisionSystem(board),
            PhysicSystem(.8),
            PlayerKillerSystem(self.game_state),

            BombExplosionSystem(self.game_state),
            LifetimeSystem(),

            BoardDisplaySystem(self.conf.image_loader, self.screen, self.conf.tile_size),
            DisplaySystem(self.conf.image_loader, self.screen),
            SpriteDisplaySystem(self.conf.image_loader, self.screen),
        ])

    def game_won(self, player: Player):
        score = self.scores[player.player_id - 1] + 1
        self.scores[player.player_id - 1] = score
        return score


def bomb_creator(game_state: GameState, avatar: Entity):
    def create(event):
        game_state.create_bomb(avatar)

    return create


def init_pygame(screen_width, screen_height):
    pg.init()
    # load and set the logo
    logo = pg.image.load("resources/bomb.png")
    pg.display.set_icon(logo)
    pg.display.set_caption('my game')
    screen = pg.display.set_mode((screen_width, screen_height))
    return screen


def run_main_menu(app: App):
    menu = pygameMenu.Menu(
        app.screen,
        *app.conf.pixel_size.data,
        font=pygameMenu.fonts.FONT_8BIT,
        title='Bomber Monkey',
        dopause=False
    )
    menu.add_option('New game', app.new_game)
    menu.add_option('Exit', PYGAME_MENU_EXIT)

    while app.app_state == AppState.MAIN_MENU:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
        menu.mainloop(events)
        pg.display.flip()


def run_pause_menu(app: App):
    menu = pygameMenu.Menu(
        app.screen,
        *app.conf.pixel_size.data,
        font=pygameMenu.fonts.FONT_8BIT,
        title='Pause',
        dopause=False
    )
    menu.add_option('Back to game', app.back_to_game)
    menu.add_option('New game', app.new_game)
    menu.add_option('Exit', PYGAME_MENU_EXIT)

    while app.app_state == AppState.PAUSE_MENU:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                app.back_to_game()
                break
        menu.mainloop(events)
        pg.display.flip()


def run_game(app: App):
    clock = pg.time.Clock()

    while app.app_state == AppState.IN_GAME:
        sim.update()
        pg.display.flip()
        clock.tick(60)
        if len(app.game_state.players) == 1:
            app.app_state = AppState.STAGE_END


def run_end_game(app: App):
    winner: Player = app.game_state.players[0].get(Player)
    score = app.game_won(winner)
    if app.conf.winning_score == score:
        run_show_winner(app, winner)
    else:
        run_show_round(app, winner)


def run_show_winner(app: App, winner: Player):
    menu = pygameMenu.TextMenu(
        app.screen,
        *app.conf.pixel_size.data,
        font=pygameMenu.fonts.FONT_8BIT,
        title='Hourrra',
        dopause=False
    )
    menu.add_line("Player %i wins this game" % winner.player_id)
    menu.add_line("")
    i = 1
    for score in app.scores:
        menu.add_line("Player %i won %s round%s" % (i, "no" if score == 0 else str(score), "s" if score > 1 else ""))
        i += 1

    while app.app_state == AppState.STAGE_END:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == pg.KEYUP and (event.key == pg.K_ESCAPE or event.key == pg.K_RETURN):
                app.app_state = AppState.MAIN_MENU
        menu.mainloop(events)
        pg.display.flip()


def run_show_round(app: App, winner: Player):
    menu = pygameMenu.TextMenu(
        app.screen,
        *app.conf.pixel_size.data,
        font=pygameMenu.fonts.FONT_8BIT,
        title='Good Job',
        dopause=False
    )
    menu.add_line("Player %i wins this round" % winner.player_id)
    menu.add_line("")
    i = 1
    for score in app.scores:
        menu.add_line("Player %i won %s round%s" % (i, "no" if score == 0 else str(score), "s" if score > 1 else ""))
        i += 1

    while app.app_state == AppState.STAGE_END:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == pg.KEYUP and (event.key == pg.K_ESCAPE or event.key == pg.K_RETURN):
                app.new_round()
        menu.mainloop(events)
        pg.display.flip()


if __name__ == "__main__":
    App().main()
