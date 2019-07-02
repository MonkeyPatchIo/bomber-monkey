import pygame as pg

from bomber_monkey.entity_factory import GameFactory
from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.game_end import GameEndState
from bomber_monkey.states.main_menu import MainMenuState
from bomber_monkey.states.pause_menu import PauseMenuState
from bomber_monkey.states.round_end import RoundEndState
from bomber_monkey.states.state_manager import StateManager


class App:
    def __init__(self):
        self.conf = GameConfig()
        self.screen = init_pygame(*self.conf.pixel_size.as_ints())

        self.state_manager = StateManager()
        self.factory = GameFactory(self.state_manager, self.conf)

        self.state_manager.init({
            AppState.MAIN_MENU: MainMenuState(self.state_manager, self.conf, self.factory, self.screen),
            AppState.IN_GAME: None,
            AppState.PAUSE_MENU: PauseMenuState(self.state_manager, self.conf, self.factory, self.screen),
            AppState.ROUND_END: RoundEndState(self.state_manager, self.conf, self.factory, self.screen),
            AppState.GAME_END: GameEndState(self.state_manager, self.conf, self.factory, self.screen),
        })

    def main(self):
        self.state_manager.change_state(AppState.MAIN_MENU)
        while True:
            self.state_manager.current_state.start()


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
