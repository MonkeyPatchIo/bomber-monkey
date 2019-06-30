import random

import pygame as pg

from bomber_monkey.entity_factory import GameFactory
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.bomb.bomb_sound_system import BombSoundSystem
from bomber_monkey.features.display.display_system import DisplaySystem, SpriteDisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.features.physics.collision_system import PlayerCollisionSystem
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.player.banana_eating_system import BananaEatingSystem
from bomber_monkey.features.player.player_controller_system import PlayerControllerSystem
from bomber_monkey.features.player.player_killer_system import PlayerKillerSystem
from bomber_monkey.features.player.player_score_display_system import PlayerScoreDisplaySystem
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.states.app_state import AppState

from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.game_end import GameEndState
from bomber_monkey.states.main_menu import MainMenuState
from bomber_monkey.states.pause_menu import PauseMenuState
from bomber_monkey.states.round_end import RoundEndState
from bomber_monkey.states.state import State


class App:
    def __init__(self):
        self.conf = GameConfig()
        self.screen = init_pygame(*self.conf.pixel_size.as_ints())
        self.factory = GameFactory(self)

        self.states = {
            AppState.MAIN_MENU: MainMenuState(self),
            AppState.IN_GAME: None,
            AppState.PAUSE_MENU: PauseMenuState(self),
            AppState.ROUND_END: RoundEndState(self),
            AppState.GAME_END: GameEndState(self),
        }
        self.current_state = None

        self.systems_provider = lambda state: [
            KeyboardSystem(),
            PlayerControllerSystem(state),
            PlayerCollisionSystem(state),
            PhysicSystem(.8),

            BombExplosionSystem(state),
            TileKillerSystem(state.board, lambda body: state.factory.create_banana(
                body) if random.random() < state.conf.banana_drop_rate else None),
            PlayerKillerSystem(state),

            BananaEatingSystem(state),
            LifetimeSystem(),

            BoardDisplaySystem(state.conf, state.conf.image_loader, state.app.screen, state.conf.tile_size),
            PlayerScoreDisplaySystem(state.conf, state.app.screen),

            DisplaySystem(state.conf, state.conf.image_loader, state.app.screen),
            SpriteDisplaySystem(state.conf, state.conf.image_loader, state.app.screen),
            BombSoundSystem(state),
        ]

    def set_state(self, state_type: AppState, state: State = None):
        if not state:
            state = self.states[state_type]

        if self.current_state:
            self.current_state.stop()
        state.init()
        self.current_state = state

    def main(self):
        self.set_state(AppState.MAIN_MENU)
        while True:
            self.current_state.start()


def init_pygame(screen_width, screen_height):
    pg.init()
    # load and set the logo
    logo = pg.image.load("resources/bomb.png")
    pg.display.set_icon(logo)
    pg.display.set_caption('Bomber Monkey')
    screen = pg.display.set_mode((screen_width, screen_height))
    return screen


if __name__ == "__main__":
    App().main()
