import pygame as pg

from bomber_monkey.features.player.players_config import PlayersConfig
from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppStateManager, AppTransitions
from bomber_monkey.states.game_end import GameEndState
from bomber_monkey.states.game_state import GameState
from bomber_monkey.states.main_menu import MainMenuState
from bomber_monkey.states.pause_menu import PauseMenuState
from bomber_monkey.states.round_end import RoundEndState


class App:
    def __init__(self):
        conf = GameConfig()
        screen = self.init_pygame(*conf.pixel_size.as_ints())
        players_config = PlayersConfig()

        main_menu_state = MainMenuState(conf, screen)

        transitions = {
            AppTransitions.MAIN_MENU: lambda _: main_menu_state,
            AppTransitions.NEW_GAME: lambda scores: GameState(conf, scores, screen, players_config),
            AppTransitions.RESUME_GAME: lambda app_state: app_state,
            AppTransitions.PAUSE_MENU: lambda game_state: PauseMenuState(conf, screen, game_state),
            AppTransitions.ROUND_END: lambda result: RoundEndState(conf, screen, players_config, result),
            AppTransitions.GAME_END: lambda result: GameEndState(conf, screen, players_config, result),
        }
        self.state_manager = AppStateManager(AppTransitions.MAIN_MENU, transitions)

    def main(self):
        pg.joystick.init()
        for _ in range(pg.joystick.get_count()):
            pg.joystick.Joystick(_).init()

        self.state_manager.run()

    @staticmethod
    def init_pygame(screen_width, screen_height):
        pg.init()
        # load and set the logo
        logo = pg.image.load("resources/bomb.png")
        pg.display.set_icon(logo)
        pg.display.set_caption('Bomber Monkey')

        # screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)
        screen = pg.display.set_mode((screen_width, screen_height))

        return screen


if __name__ == "__main__":
    App().main()
