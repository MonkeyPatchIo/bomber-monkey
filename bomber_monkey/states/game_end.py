import time
from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
from pygame.surface import Surface

from bomber_monkey.features.display.score_board import ScoreBoard
from bomber_monkey.features.player.players_config import PlayersConfig
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_scores import GameRoundResult
from bomber_monkey.states.app_state import AppState, AppTransition, AppTransitions


class GameEndTransition(AppTransition):
    def __init__(self, conf: GameConfig, screen: Surface, players_config: PlayersConfig):
        super().__init__()
        self.conf = conf
        self.screen = screen
        self.players_config = players_config

    def next_state(self, result: GameRoundResult) -> AppState:
        return GameEndState(self.conf, self.screen, self.players_config, result)


class GameEndState(AppState):

    def __init__(self, conf: GameConfig, screen: Surface, players_config: PlayersConfig, result: GameRoundResult):
        super().__init__()
        self.result = result
        title = "Player {} wins".format(result.winner_id + 1)
        self.score_board = ScoreBoard(conf, screen, players_config, result, title)
        self.allow_quit_time = time.time() + conf.score_board_min_display_time

    def run(self) -> Tuple[IntEnum, Any]:
        events = pg.event.get()
        if time.time() > self.allow_quit_time:
            for event in events:
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYUP and (event.key == pg.K_ESCAPE or event.key == pg.K_RETURN):
                    return AppTransitions.MAIN_MENU, None
        self.score_board.draw_scores()
        pg.display.flip()
