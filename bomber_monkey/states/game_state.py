from typing import List

import pygame as pg

from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.bomb.bomb_sound_system import BombSoundSystem
from bomber_monkey.features.display.display_system import DisplaySystem, SpriteDisplaySystem
from bomber_monkey.features.display.fps_display_system import FpsDisplaySystem
from bomber_monkey.features.display.score_display_system import PlayerScoreDisplaySystem
from bomber_monkey.features.display.title_displaysystem import TitleDisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.features.physics.collision_system import PlayerCollisionSystem
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.player.banana_eating_system import BananaEatingSystem
from bomber_monkey.features.player.player_controller_system import PlayerControllerSystem
from bomber_monkey.features.player.player_killer_system import PlayerKillerSystem
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.features.board.board import Board
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller import PlayerController
from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State
from bomber_monkey.states.state_manager import StateManager
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Entity, Simulator


class GameState(State):
    clock = pg.time.Clock()

    def __init__(self,
                 state_manager: StateManager,
                 conf: GameConfig,
                 screen
                 ):
        super().__init__()
        self.state_manager = state_manager
        self.conf = conf
        self.factory = GameFactory(state_manager, conf)
        self.screen = screen
        self._board: Board = None
        self._players: List[Entity] = []
        self.scores = [0] * 2
        self._sim = Simulator()

    @property
    def sim(self):
        return self._sim

    @property
    def players(self) -> list:
        return self._players

    @property
    def board(self) -> Board:
        return self._board

    def init(self):
        self.sim.reset()
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
        self.sim.create(Keymap({
            pg.K_ESCAPE: (None, lambda e: self.state_manager.change_state(AppState.PAUSE_MENU)),
        }))

        # init simulation (ECS)
        self.sim.reset_systems([
            KeyboardSystem(),
            PlayerControllerSystem(),
            PlayerCollisionSystem(self.board),
            PhysicSystem(.8),

            BombExplosionSystem(self.factory),
            TileKillerSystem(self.board, lambda body: self.factory.create_banana(body, self.conf.banana_drop_rate)),
            PlayerKillerSystem(self.factory),

            BananaEatingSystem(self.factory),
            LifetimeSystem(),

            BoardDisplaySystem(self.conf, self.conf.image_loader, self.screen, self.conf.tile_size),
            TitleDisplaySystem(self.conf, self.screen),
            PlayerScoreDisplaySystem(self.factory, self.screen),
            FpsDisplaySystem(self.factory, self.screen),

            DisplaySystem(self.conf, self.screen),
            SpriteDisplaySystem(self.conf, self.screen),
            BombSoundSystem(),

        ])

    def _run(self):
        self.sim.update()
        if len(self.players) == 1:
            self.run_end_game()

        pg.display.flip()
        GameState.clock.tick(60)

    def run_end_game(self):
        winner: Player = self.players[0].get(Player)
        self.scores[winner.player_id] += 1

        if self.scores[winner.player_id] == self.conf.winning_score:
            next_state = AppState.GAME_END
        else:
            next_state = AppState.ROUND_END

        self.state_manager.states[next_state].winner = winner
        self.state_manager.change_state(next_state)
