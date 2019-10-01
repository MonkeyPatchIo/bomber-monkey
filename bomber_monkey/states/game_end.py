import time
from enum import IntEnum
from typing import Tuple, Any

import pygame
from pygame.surface import Surface

from bomber_monkey.features.display.score_board import ScoreBoard
from bomber_monkey.features.player.player_controller import PlayerAction
from bomber_monkey.features.player.players_config import PlayersConfig
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_scores import GameRoundResult
from bomber_monkey.states.app_state import AppState, AppTransitions


class GameEndState(AppState):

    def __init__(self, conf: GameConfig, screen: Surface, players_config: PlayersConfig, result: GameRoundResult):
        super().__init__()
        self.players_config = players_config
        self.result = result
        title = "Player {} wins".format(result.winner_id + 1)
        self.score_board = ScoreBoard(conf, screen, players_config, result, title)
        self.allow_quit_time = time.time() + conf.score_board_min_display_time

    def run(self) -> Tuple[IntEnum, Any]:
        events = pygame.event.get()
        if time.time() > self.allow_quit_time:
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.JOYAXISMOTION or event.type == pygame.KEYUP:
                    key = event.key if event.type == pygame.KEYUP else None
                    for descriptor in self.players_config.descriptors:
                        action = descriptor.actioner(key)
                        if action & PlayerAction.SPECIAL_ACTION:
                            return AppTransitions.MAIN_MENU, None
        self.score_board.draw_scores()
        pygame.display.flip()
