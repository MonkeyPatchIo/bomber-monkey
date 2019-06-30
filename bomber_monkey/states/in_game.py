from typing import List

import pygame as pg

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller import PlayerController
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import sim, Entity


class GameState(State):
    clock = pg.time.Clock()

    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app
        self.conf = app.conf
        self._board: Board = None
        self._players: List[Entity] = []
        self.scores = [0] * 2

        self.factory = app.factory
        self.systems_provider = app.systems_provider

    @property
    def players(self) -> list:
        return self._players

    @property
    def board(self) -> Board:
        return self._board

    def init(self):
        sim.reset()
        self.factory.create_board()

        self._players = [
            self.factory.create_player(
                player_id=0,
                grid_pos=Vector.create(1, 1),
                controller=PlayerController(
                    down_key=pg.K_s,
                    up_key=pg.K_z,
                    left_key=pg.K_q,
                    right_key=pg.K_d,
                    action_key=pg.K_SPACE
                )
            ),
            self.factory.create_player(
                player_id=1,
                grid_pos=Vector.create(self.board.width - 2, self.board.height - 2),
                controller=PlayerController(
                    down_key=pg.K_DOWN,
                    up_key=pg.K_UP,
                    left_key=pg.K_LEFT,
                    right_key=pg.K_RIGHT,
                    action_key=pg.K_KP0
                ))
        ]

        # create heyboard handlers
        sim.create(Keymap({
            pg.K_ESCAPE: (None, lambda e: self.app.change_state(AppState.PAUSE_MENU)),
        }))

        # init simulation (ECS)
        sim.reset_systems(self.systems_provider(self))

    def _run(self):
        sim.update()
        pg.display.flip()
        GameState.clock.tick(60)
        if len(self.app.states[AppState.IN_GAME].players) == 1:
            self.run_end_game()

    def run_end_game(self):
        winner: Player = self.app.states[AppState.IN_GAME].players[0].get(Player)
        self.scores[winner.player_id] += 1

        if self.scores[winner.player_id] == self.app.conf.winning_score:
            next_state = AppState.GAME_END
        else:
            next_state = AppState.ROUND_END

        self.app.states[next_state].winner = winner
        self.app.change_state(next_state)
