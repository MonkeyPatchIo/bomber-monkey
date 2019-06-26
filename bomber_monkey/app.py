from enum import IntEnum

import pygame as pg
import pygameMenu
from bomber_monkey.features.bomb.bomb_dropper import BombDropper
from bomber_monkey.features.bomb.wall_explosion_system import WallExplosionSystem
from bomber_monkey.features.score.score_display_system import ScoresDisplaySystem
from bomber_monkey.features.score.scores import Scores
from pygame.locals import *
from pygameMenu.locals import *

from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.bomb.player_killer_system import PlayerKillerSystem
from bomber_monkey.features.display.display_system import DisplaySystem, SpriteDisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.features.physics.collision_system import PlayerCollisionSystem
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller import PlayerController
from bomber_monkey.features.player.player_controller_system import PlayerControllerSystem
from bomber_monkey.game_config import GameConfig
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
        self.conf = GameConfig()
        self.app_state = AppState.MAIN_MENU
        self.screen = init_pygame(*self.conf.pixel_size.as_ints())
        self.scores: Scores = None
        self.game_state: GameState = None

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
        self.scores = Scores([0] * 2)
        self.new_round()

    def new_round(self):
        self.app_state = AppState.IN_GAME
        sim.reset()
        self.game_state = GameState(self.conf)

        sim.create(self.scores)
        self.game_state.create_board()

        self.game_state.create_player(
            Vector.create(1, 1),
            controller=PlayerController(
                down_key=pg.K_s,
                up_key=pg.K_z,
                left_key=pg.K_q,
                right_key=pg.K_d,
                action_key=pg.K_SPACE
            )
        )
        self.game_state.create_player(
            Vector.create(self.game_state.board.width - 2, self.game_state.board.height - 2),
            controller=PlayerController(
                down_key=pg.K_DOWN,
                up_key=pg.K_UP,
                left_key=pg.K_LEFT,
                right_key=pg.K_RIGHT,
                action_key=pg.K_RETURN
            ))

        accel = 1

        # create heyboard handlers
        sim.create(Keymap({
            pg.K_ESCAPE: (None, lambda e: self.pause_game()),
        }))

        # init simulation (ECS)
        sim.reset_systems([
            KeyboardSystem(),
            PlayerControllerSystem(self.game_state),

            PlayerCollisionSystem(self.game_state),
            PhysicSystem(.8),

            BombExplosionSystem(self.game_state),
            WallExplosionSystem(self.game_state.board),
            PlayerKillerSystem(self.game_state),
            LifetimeSystem(),

            ScoresDisplaySystem(self.conf, self.screen),
            BoardDisplaySystem(self.conf, self.conf.image_loader, self.screen, self.conf.tile_size),
            DisplaySystem(self.conf, self.conf.image_loader, self.screen),
            SpriteDisplaySystem(self.conf, self.conf.image_loader, self.screen),
        ])

    def game_won(self, player: Player):
        score = self.scores.scores[player.player_id - 1] + 1
        self.scores.scores[player.player_id - 1] = score
        return score


def bomb_creator(game_state: GameState, avatar: Entity):
    def create(event):
        body: RigidBody = avatar.get(RigidBody)
        bomber: BombDropper = avatar.get(BombDropper)
        if bomber.drop():
            game_state.create_bomb(body)

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
        *app.conf.pixel_size.as_ints(),
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
        *app.conf.pixel_size.as_ints(),
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
        *app.conf.pixel_size.as_ints(),
        font=pygameMenu.fonts.FONT_8BIT,
        title='Hourrra',
        dopause=False
    )
    menu.add_line("Player %i wins" % winner.player_id)

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
        *app.conf.pixel_size.as_ints(),
        font=pygameMenu.fonts.FONT_8BIT,
        title='Good Job',
        dopause=False
    )
    menu.add_line("Player %i scored" % winner.player_id)

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
