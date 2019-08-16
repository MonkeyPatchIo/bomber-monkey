from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
import pygameMenu

from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_scores import GameScores
from bomber_monkey.states.app_state import AppState, AppTransition, AppTransitions


class GameEndTransition(AppTransition):
    def __init__(self, conf: GameConfig, screen):
        super().__init__()
        self.conf = conf
        self.screen = screen

    def next_state(self, scores: GameScores) -> AppState:
        return GameEndState(self.conf, self.screen, scores)


class GameEndState(AppState):

    def __init__(self, conf: GameConfig, screen, scores: GameScores = None):
        super().__init__()
        self.menu = pygameMenu.TextMenu(
            screen,
            *conf.pixel_size.as_ints(),
            font=pygameMenu.font.FONT_8BIT,
            title='Hourrra',
            dopause=False
        )
        winner = scores.scores.index(max(scores.scores))
        self.menu.add_line("Player {} wins".format(winner))

    def run(self) -> Tuple[IntEnum, Any]:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYUP and (event.key == pg.K_ESCAPE or event.key == pg.K_RETURN):
                return AppTransitions.MAIN_MENU, None
        self.menu.mainloop(events)
        pg.display.flip()
