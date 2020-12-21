from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
import pygame_menu

from bomber_monkey.game_config import GameConfig, MENU_THEME, MENU_FONT_SIZE
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
        self.menu.add_button('Resume', self.resume_game)
        self.menu.add_button('Quit', self.quit_game)

    def resume_game(self):
        self.transition = (AppTransitions.RESUME_GAME, self.game_state)

    def quit_game(self):
        self.transition = (AppTransitions.MAIN_MENU, None)

    def run(self) -> Tuple[IntEnum, Any]:
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYUP and event.key in [pg.K_ESCAPE]:
                self.resume_game()
        self.menu.update(events)
        self.menu.draw(self.screen)
        pg.display.flip()
        transition = self.transition
        self.transition = None
        return transition
