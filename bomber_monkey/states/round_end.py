from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
import pygameMenu

from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState, AppTransition, AppTransitions


class RoundEndTransition(AppTransition):
    def __init__(self, conf: GameConfig, screen):
        super().__init__()
        self.conf = conf
        self.screen = screen

    def next_state(self, winner) -> AppState:
        return RoundEndState(self.conf, self.screen, winner)


class RoundEndState(AppState):
    def __init__(self, conf: GameConfig, screen, winner: Player = None):
        super().__init__()
        self.menu = pygameMenu.TextMenu(
            screen,
            *conf.pixel_size.as_ints(),
            font=pygameMenu.font.FONT_8BIT,
            title='Good Job',
            dopause=False
        )
        if winner:
            message = "Player {} scored".format(winner.player_id)
        else:
            message = "DRAW !!"

        self.menu.add_line(message)

    def run(self) -> Tuple[IntEnum, Any]:
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYUP or event.type == pg.JOYBUTTONUP:
                return AppTransitions.NEW_GAME, None
        self.menu.mainloop(events)
        pg.display.flip()
