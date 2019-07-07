from typing import List

import pygame as pg

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.bomb.bomb_sound_system import BombSoundSystem
from bomber_monkey.features.destruction.destruction_system import DestructionSystem
from bomber_monkey.features.destruction.protection_system import ProtectionSystem
from bomber_monkey.features.display.image_display_system import ImageDisplaySystem
from bomber_monkey.features.display.score_display_system import PlayerScoreDisplaySystem
from bomber_monkey.features.display.sprite_display_system import SpriteDisplaySystem
from bomber_monkey.features.display.title_bar_display_system import TitleBarDisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.features.physics.collision_system import PlayerCollisionSystem
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.player.banana_eating_system import BananaEatingSystem
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller_system import PlayerControllerSystem
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State
from bomber_monkey.states.state_manager import StateManager
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator


class GameState(State):
    clock = pg.time.Clock()

    def __init__(self,
                 state_manager: StateManager,
                 conf: GameConfig,
                 screen=None,
                 controllers=None
                 ):
        super().__init__()
        self.state_manager = state_manager
        self.conf = conf
        self.factory = GameFactory(state_manager, conf)
        self._board: Board = None
        self.scores: List[int] = [0] * 4
        self._sim = Simulator(context=self)

        self.state_manager.states[AppState.IN_GAME] = self
        self.screen = screen
        self.controllers = controllers or [None] * 10

    @property
    def sim(self):
        return self._sim

    @property
    def board(self) -> Board:
        return self._board

    def init(self):
        self.sim.reset()
        self._board = self.factory.create_board()

        slots = [
            PlayerSlot(
                player_id=0,
                start_pos=Vector.create(1, 1),
                color=(255, 0, 0),
                score_pos=(5, 3)
            ),

            PlayerSlot(
                player_id=1,
                start_pos=Vector.create(self.board.width - 2, self.board.height - 2),
                color=(0, 0, 255),
                score_pos=(self.conf.pixel_size.x - 45, 3 + 45)
            ),
            PlayerSlot(
                player_id=2,
                start_pos=Vector.create(1, self.board.height - 2),
                color=(0, 255, 0),
                score_pos=(5, 3 + 45)
            ),
            PlayerSlot(
                player_id=3,
                start_pos=Vector.create(self.board.width - 2, 1),
                color=(255, 255, 0),
                score_pos=(self.conf.pixel_size.x - 45, 3)
            )
        ]

        player_perm = self.conf.PLAYER_PERMUTATION[:self.conf.PLAYER_NUMBER]

        for i, j in enumerate(player_perm):
            self.factory.create_player(
                slot=slots[i],
                controller=self.controllers[j]
            )

        # create heyboard handlers
        self.sim.create(Keymap({
            pg.K_ESCAPE: (None, lambda e: self.state_manager.change_state(AppState.PAUSE_MENU)),
        }))

        # init simulation (ECS)
        display_systems = [
            BoardDisplaySystem(self.conf, self.screen),
            TitleBarDisplaySystem(self.conf, self.screen),
            PlayerScoreDisplaySystem(self.screen),
            ImageDisplaySystem(self.conf, self.screen),
            SpriteDisplaySystem(self.conf, self.screen),
            BombSoundSystem(),
        ] if self.screen else []

        self.sim.reset_systems([
            KeyboardSystem(),
            PlayerControllerSystem(),

            PlayerCollisionSystem(),
            PhysicSystem(.8),

            BombExplosionSystem(),
            TileKillerSystem(lambda body: self.factory.create_banana(body, self.conf.banana_drop_rate)),
            DestructionSystem(),
            ProtectionSystem(),

            BananaEatingSystem(),
            LifetimeSystem(),

            *display_systems,
        ])

    def _run(self):
        self.sim.update()
        self.check_endgame()
        pg.display.flip()
        GameState.clock.tick(self.conf.MAX_FPS)

    def check_endgame(self):
        if len(self.board.players) == 0:
            next_state = AppState.ROUND_END
            self.state_manager.states[next_state].winner = None
            self.state_manager.change_state(next_state)

        if len(self.board.players) == 1:
            winner: Player = self.board.players[0].get(Player)
            self.scores[winner.player_id] += 1

            if self.scores[winner.player_id] == self.conf.winning_score:
                next_state = AppState.GAME_END
            else:
                next_state = AppState.ROUND_END

            self.state_manager.states[next_state].winner = winner
            self.state_manager.change_state(next_state)
