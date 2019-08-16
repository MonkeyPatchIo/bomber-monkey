import pygame as pg

import bomber_monkey.states.game_end
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_scores import GameScores
from bomber_monkey.states.app_state import StateLessAppTransition, AppStateManager, AppTransitions
from bomber_monkey.states.game_state import NewGameTransition, ResumeGameTransition
from bomber_monkey.states.main_menu import MainMenuState
from bomber_monkey.states.pause_menu import EnterPauseTransition
from bomber_monkey.states.round_end import RoundEndTransition


class App:
    def __init__(self):
        conf = GameConfig()
        scores = GameScores(conf)
        screen = self.init_pygame(*conf.pixel_size.as_ints())

        transitions = {
            AppTransitions.MAIN_MENU: StateLessAppTransition(MainMenuState(conf, screen)),
            AppTransitions.NEW_GAME: NewGameTransition(conf, screen),
            AppTransitions.RESUME_GAME: ResumeGameTransition(),
            AppTransitions.PAUSE_MENU: EnterPauseTransition(conf, screen),
            AppTransitions.ROUND_END: RoundEndTransition(conf, screen),
            AppTransitions.GAME_END: bomber_monkey.states.game_end.GameEndTransition(conf, screen),
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
