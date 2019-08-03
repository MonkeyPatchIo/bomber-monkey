from enum import IntEnum
from typing import List, Tuple, Any

import pygame as pg

import bomber_monkey
from bomber_monkey.config_controller import controller_provider
from bomber_monkey.features.board.board import Board
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem, ExplosionPropagationSystem
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
from bomber_monkey.features.physics.collision_physic import PlayerCollisionWithDTPhysic
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.player.banana_eating_system import BananaEatingSystem
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller_system import PlayerControllerSystem
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.states.app_state import AppState, AppTransition, AppTransitions
from python_ecs.ecs import Simulator


class NewGameTransition(AppTransition):
    def __init__(self, conf: GameConfig, screen):
        self.conf = conf
        self.screen = screen

    def next_state(self, context) -> AppState:
        return GameState(self.conf, self.screen, controller_provider(self.conf))


class ResumeGameTransition(AppTransition):

    def next_state(self, context) -> AppState:
        return context


class GameState(AppState):
    clock = pg.time.Clock()

    def __init__(self,
                 conf: GameConfig,
                 screen=None,
                 controllers=None
                 ):
        super().__init__()
        self.conf = conf
        self.transition = None
        self.controllers = controllers
        self.scores: List[int] = [0] * 4
        self._sim = Simulator(context=self)
        self.sim.reset()
        self._board = GameFactory.create_board(self.sim)

        # create players
        slots = self.conf.player_slots(self.board)
        player_perm = self.conf.PLAYER_PERMUTATION[:self.conf.PLAYER_NUMBER]
        for i, j in enumerate(player_perm):
            GameFactory.create_player(
                self.sim,
                slot=slots[i],
                controller=self.controllers[j]
            )

        # create keyboard handlers
        self.sim.create(Keymap({
            pg.K_ESCAPE: (None, self.pause_game),
        }))

        systems = [
            KeyboardSystem(),
            PlayerControllerSystem(),

            PhysicSystem(PlayerCollisionWithDTPhysic()),

            BombExplosionSystem(),
            ExplosionPropagationSystem(),
            TileKillerSystem(lambda body: GameFactory.create_banana(self.sim, body, self.conf.banana_drop_rate)),
            DestructionSystem(),
            ProtectionSystem(),

            BananaEatingSystem(),
            LifetimeSystem()
        ]

        display_systems = [
            BoardDisplaySystem(self.conf, screen),
            TitleBarDisplaySystem(screen),
            PlayerScoreDisplaySystem(screen),
            ImageDisplaySystem(self.conf, screen),
            SpriteDisplaySystem(self.conf, screen),
            BombSoundSystem(),
        ]

        # init simulation (ECS)
        self.sim.reset_systems([
            *systems,
            *display_systems,
        ])

    @property
    def sim(self):
        return self._sim

    @property
    def board(self) -> Board:
        return self._board

    def pause_game(self, event):
        self.transition = (AppTransitions.PAUSE_MENU, self)

    def run(self) -> Tuple[IntEnum, Any]:
        self.sim.update()
        pg.display.flip()
        GameState.clock.tick(self.conf.MAX_FPS)

        if len(self.board.players) == 0:
            return AppTransitions.ROUND_END, None

        if len(self.board.players) == 1:
            winner: Player = self.board.players[0].get(Player)
            self.scores[winner.player_id] += 1

            if self.scores[winner.player_id] == self.conf.winning_score:
                return AppTransitions.GAME_END, winner
            return AppTransitions.ROUND_END, winner

        return self.transition
