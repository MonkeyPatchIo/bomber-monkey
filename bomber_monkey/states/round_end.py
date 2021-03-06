import time
from enum import IntEnum
from typing import Tuple, Any

import pygame
from pygame.surface import Surface

from bomber_monkey.features.display.score_board import ScoreBoard
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.features.player.players_config import PlayersConfig, menu_wait
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_scores import GameRoundResult
from bomber_monkey.states.app_state import AppState, AppTransitions


class RoundEndState(AppState):
    def __init__(self, conf: GameConfig, screen: Surface, players_config: PlayersConfig, result: GameRoundResult):
        super().__init__()
        self.players_config = players_config
        self.result = result
        if self.result.winner_id is not None:
            title = "Player {} scored".format(self.result.winner_id + 1)
        else:
            title = "DRAW"
        self.score_board = ScoreBoard(conf, screen, players_config, result, title)
        self.allow_quit_time = time.time() + conf.score_board_min_display_time

    def run(self) -> Tuple[IntEnum, Any]:
        if time.time() > self.allow_quit_time:
            for player_id, action in menu_wait(self.players_config):
                if action & PlayerAction.MAIN_ACTION:
                    return AppTransitions.NEW_GAME, self.result.scores
        self.score_board.draw_scores()
        pygame.display.flip()
