from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
import pygameMenu

from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_scores import GameScores
from bomber_monkey.states.app_state import AppState, AppTransitions


class MainMenuState(AppState):
    def __init__(self, conf: GameConfig, screen):
        super().__init__()
        self.conf = conf
        self.screen = screen
        self.transition = None
        self.menu = pygameMenu.Menu(
            screen,
            *conf.pixel_size.as_ints(),
            font=pygameMenu.font.FONT_8BIT,
            title='Bomber Monkey',
            dopause=False
        )
        self.menu.add_option('New game', self.new_game)
        self.menu.add_option('Exit', pygameMenu.events.EXIT)

    def new_game(self):
        self.transition = (AppTransitions.NEW_GAME, GameScores(self.conf))

    def run(self) -> Tuple[IntEnum, Any]:
        events = pg.event.get()
        # clean screen
        self.screen.fill((0, 0, 0), pg.rect.Rect((0, 0), self.conf.pixel_size.as_ints()))
        self.menu.mainloop(events)
        pg.display.flip()
        transition = self.transition
        self.transition = None
        return transition
