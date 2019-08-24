import time
from enum import IntEnum
from typing import Tuple, Any

import pygame as pg
from pygame.surface import Surface

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem, ExplosionPropagationSystem
from bomber_monkey.features.bomb.bomb_sound_system import BombSoundSystem
from bomber_monkey.features.destruction.destruction_system import DestructionSystem
from bomber_monkey.features.destruction.protection_system import ProtectionSystem
from bomber_monkey.features.display.image_display_system import ImageDisplaySystem
from bomber_monkey.features.display.score_display_system import PlayerScoreDisplaySystem
from bomber_monkey.features.display.sprite_display_system import SpriteDisplaySystem
from bomber_monkey.features.display.startup_count_down_display_system import StartupCountDownDisplaySystem
from bomber_monkey.features.display.title_bar_display_system import TitleBarDisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.features.physics.collision_physic import PlayerCollisionWithDTPhysic
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.player.banana_eating_system import BananaEatingSystem
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller_system import PlayerControllerSystem
from bomber_monkey.features.player.players_config import PlayersConfig
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.game_scores import GameScores, GameRoundResult
from bomber_monkey.states.app_state import AppState, AppTransitions
from python_ecs.ecs import Simulator


class GameState(AppState):

    def __init__(self,
                 conf: GameConfig,
                 scores: GameScores,
                 screen: Surface,
                 player_config: PlayersConfig
                 ):
        super().__init__()
        self.conf = conf
        self.transition = None
        self.scores = scores if scores is not None else GameScores(player_config.nb_players)
        self._sim = Simulator(context=self)
        self.sim.reset()
        self._board = GameFactory.create_board(self.sim)
        self.clock = pg.time.Clock()
        self.start_time = time.time()
        self.pause_start_time = -1
        self.paused_time = 0

        for slot, actioner in player_config.slot_and_actioners:
            GameFactory.create_player(self.sim, slot, actioner)

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
            TitleBarDisplaySystem(self.conf, screen),
            PlayerScoreDisplaySystem(screen),
            ImageDisplaySystem(self.conf, screen),
            SpriteDisplaySystem(self.conf, screen, 0),
            SpriteDisplaySystem(self.conf, screen, 1),
            StartupCountDownDisplaySystem(screen),
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

    @property
    def game_elapsed_time(self):
        return time.time() - self.start_time - self.paused_time

    def pause_game(self, event):
        self.pause_start_time = time.time()
        self.transition = (AppTransitions.PAUSE_MENU, self)

    def run(self) -> Tuple[IntEnum, Any]:
        if self.pause_start_time > 0:
            # we are getting out of a pause
            self.paused_time += time.time() - self.pause_start_time
            self.pause_start_time = -1
        self.sim.update()
        pg.display.flip()
        self.clock.tick(self.conf.MAX_FPS)

        if len(self.board.players) == 0:
            return AppTransitions.ROUND_END, GameRoundResult(self.scores, None)

        if len(self.board.players) == 1:
            winner: Player = self.board.players[0].get(Player)
            self.scores.scores[winner.player_id] += 1

            if self.scores.scores[winner.player_id] == self.conf.winning_score:
                return AppTransitions.GAME_END, GameRoundResult(self.scores, winner.player_id)
            return AppTransitions.ROUND_END, GameRoundResult(self.scores, winner.player_id)

        transition = self.transition
        self.transition = None
        return transition
