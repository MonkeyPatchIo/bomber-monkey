from enum import IntEnum
from typing import Tuple, Any

import pygame as pg

from bomber_monkey.features.display.score_board import ScoreBoard
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_scores import GameRoundResult
from bomber_monkey.states.app_state import AppState, AppTransition, AppTransitions


class GameEndTransition(AppTransition):
    def __init__(self, conf: GameConfig, screen):
        super().__init__()
        self.conf = conf
        self.screen = screen

    def next_state(self, result: GameRoundResult) -> AppState:
        return GameEndState(self.conf, self.screen, result)


class GameEndState(AppState):

    def __init__(self, conf: GameConfig, screen, result: GameRoundResult):
        super().__init__()
        self.result = result
        title = "Player {} wins".format(result.winner_id + 1)
        self.score_board = ScoreBoard(conf, screen, result, title)

    def run(self) -> Tuple[IntEnum, Any]:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYUP and (event.key == pg.K_ESCAPE or event.key == pg.K_RETURN):
                return AppTransitions.MAIN_MENU, None
        self.score_board.draw_scores()
        pg.display.flip()
