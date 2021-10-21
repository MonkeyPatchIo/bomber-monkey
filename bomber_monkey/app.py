from pathlib import Path

import pygame

from bomber_monkey.config import setup_logs
from bomber_monkey.controllers_configurator import ControllersConfigurator
from bomber_monkey.states.app_state import AppStateManager, AppTransitions
from bomber_monkey.states.game_end import GameEndState
from bomber_monkey.states.game_state import GameState
from bomber_monkey.states.main_menu import MainMenuState
from bomber_monkey.states.pause_menu import PauseMenuState
from bomber_monkey.states.round_end import RoundEndState
from bomber_monkey.utils.joystick import init_joysticks
from bomber_monkey.utils.timing import setup_timing, show_timing


def main():
    pygame.init()
    pygame.joystick.init()
    init_joysticks()

    logo = pygame.image.load("resources/bomb.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Bomber Monkey')

    configurator = ControllersConfigurator()
    configurator.run()

    conf = configurator.conf
    players_config = configurator.players_config

    screen = pygame.display.set_mode(conf.pixel_size.as_ints(),
                                     (pygame.FULLSCREEN + pygame.SCALED) if conf.fullscreen else 0)
    main_menu_state = MainMenuState(conf, screen, players_config)

    transitions = {
        AppTransitions.MAIN_MENU: lambda _: main_menu_state,
        AppTransitions.NEW_GAME: lambda scores: GameState(conf, scores, screen, players_config),
        AppTransitions.RESUME_GAME: lambda app_state: app_state,
        AppTransitions.PAUSE_MENU: lambda game_state: PauseMenuState(screen, game_state),
        AppTransitions.ROUND_END: lambda result: RoundEndState(conf, screen, players_config, result),
        AppTransitions.GAME_END: lambda result: GameEndState(conf, screen, players_config, result),
    }
    state_manager = AppStateManager(AppTransitions.MAIN_MENU, transitions)

    state_manager.run()


if __name__ == "__main__":
    setup_logs(config_path=Path('resources/config.json'))
    setup_timing()
    try:
        main()
    finally:
        show_timing()
