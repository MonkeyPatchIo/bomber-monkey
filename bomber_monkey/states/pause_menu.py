from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
import pygameMenu

from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState, AppTransition, AppTransitions
from bomber_monkey.states.game_state import GameState


class EnterPauseTransition(AppTransition):
    def __init__(self, conf: GameConfig, screen):
        super().__init__()
        self.conf = conf
        self.screen = screen

    def next_state(self, game_state) -> AppState:
        return PauseMenuState(self.conf, self.screen, game_state)


class PauseMenuState(AppState):
    def __init__(self, conf: GameConfig, screen, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.transition = None
        self.menu = pygameMenu.Menu(
            screen,
            *conf.pixel_size.as_ints(),
            font=pygameMenu.font.FONT_8BIT,
            title='Pause',
            dopause=False
        )
        self.menu.add_option('Back to game', self.resume_game)
        self.menu.add_option('Main menu', self.quit_game)
        self.menu.add_option('Exit', pygameMenu.events.EXIT)

    def resume_game(self):
        self.transition = (AppTransitions.RESUME_GAME, self.game_state)

    def quit_game(self):
        self.transition = (AppTransitions.MAIN_MENU, None)

    def run(self) -> Tuple[IntEnum, Any]:
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYUP and event.key not in [pg.K_UP, pg.K_DOWN]:
                self.resume_game()
        self.menu.mainloop(events)
        pg.display.flip()
        transition = self.transition
        self.transition = None
        return transition
