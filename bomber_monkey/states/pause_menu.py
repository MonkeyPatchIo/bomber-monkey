from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
import pygame_menu

from bomber_monkey.game_config import MENU_THEME, MENU_FONT_SIZE
from bomber_monkey.game_inputs import get_game_inputs
from bomber_monkey.states.app_state import AppState, AppTransitions
from bomber_monkey.states.game_state import GameState


class PauseMenuState(AppState):
    def __init__(self, screen, game_state: GameState):
        super().__init__()
        self.screen = screen
        self.game_state = game_state
        self.transition = None
        self.menu = pygame_menu.Menu(
            height=MENU_FONT_SIZE * 5,
            width=MENU_FONT_SIZE * 15,
            theme=MENU_THEME,
            title='Pause'
        )
        self.menu.add.button('Resume', self.resume_game)
        self.menu.add.button('Quit', self.quit_game)

    def resume_game(self):
        self.transition = (AppTransitions.RESUME_GAME, self.game_state)

    def quit_game(self):
        self.transition = (AppTransitions.MAIN_MENU, None)

    def run(self) -> Tuple[IntEnum, Any]:
        inputs = get_game_inputs()
        if inputs.is_up(pg.K_ESCAPE):
            self.resume_game()
        self.menu.update(inputs.events)
        self.menu.draw(self.screen)
        pg.display.flip()
        transition = self.transition
        self.transition = None
        return transition
