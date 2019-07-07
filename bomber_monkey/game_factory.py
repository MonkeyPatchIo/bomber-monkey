import random
from typing import List

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.board.board import Tiles, Board, random_blocks, clear_corners, wall_grid, fill_border, \
    clear_center
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller import PlayerController
from bomber_monkey.features.destruction.destruction import Destruction, Protection
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.features.spawner.spawner import Spawner
from bomber_monkey.features.tile.tile_killer import TileKiller
from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.state_manager import StateManager
from bomber_monkey.states.app_state import AppState
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Entity, Simulator


class GameFactory(object):

    def __init__(self, state_manager: StateManager, conf: GameConfig):
        super().__init__()
        self.state_manager = state_manager
        self.conf = conf

    @property
    def game_state(self) -> 'GameState':
        return self.state_manager.states[AppState.IN_GAME]

    @property
    def sim(self) -> Simulator:
        return self.game_state.sim

    @property
    def board(self) -> Board:
        return self.game_state.board

    def create_player(self, slot: PlayerSlot, controller: PlayerController):
        pos = slot.start_pos * self.conf.tile_size + self.conf.tile_size // 2

        sprite = Sprite(
            image_id=slot.player_id,
            path=self.conf.media_path('monkey_sprite.png'),
            size=self.conf.tile_size,
            sprite_size=Vector.create(40, 36),
            anim_size=10,
        )
        sprite.change_color(self.conf.image_loader, slot.color)

        player = self.sim.create(
            RigidBody(
                pos=pos,
                shape=Shape(self.conf.tile_size),
            ),
            sprite,
            Player(slot, self.conf.bomb_power),
            Spawner(self.conf.bomb_drop_rate, self.create_bomb),
            controller
        )

        return player

    def create_explosion(self, pos: Vector):
        return self.sim.create(
            RigidBody(
                pos=pos,
                shape=Shape(self.conf.tile_size // 2),
            ),
            Image(
                self.conf.media_path('fire.png'),
                size=self.conf.tile_size // 2,
            ),
            Lifetime(self.conf.explosion_duration),
            Destruction(),
            TileKiller(Tiles.BLOCK)
        )

    def create_board(self):
        board = Board(tile_size=self.conf.tile_size, grid_size=self.conf.grid_size)
        self.sim.on_create.append(board.on_create)
        self.sim.on_destroy.append(board.on_destroy)

        random_blocks(board, Tiles.BLOCK, 1.)
        # random_blocks(board, Tiles.WALL, .5)
        clear_corners(board)
        clear_center(board)

        wall_grid(board)

        fill_border(board, Tiles.WALL)
        self.sim.create(board)

        return board

    def create_banana(self, body: RigidBody, probability: float = 1):
        if random.random() > probability:
            return None

        return self.sim.create(
            RigidBody(
                pos=self.board.by_pixel(body.pos).center,
                shape=Shape(self.conf.tile_size),
            ),
            Sprite(
                self.conf.media_path('banana_sprite32.png'),
                size=self.conf.tile_size,
                sprite_size=Vector.create(32, 32),
                anim_size=11,
                anim_time=.5
            ),
            Banana(),
            Protection(duration=self.conf.explosion_duration * 2)
        )

    def create_bomb(self, body: RigidBody):
        player: Player = body.entity().get(Player)
        power = player.power if player else self.conf.bomb_power

        return self.sim.create(
            RigidBody(
                pos=self.board.by_pixel(body.pos).center,
                shape=Shape(self.conf.tile_size),
            ),
            Sprite(
                self.conf.media_path('bomb_sprite.png'),
                size=self.conf.tile_size * 2,
                sprite_size=Vector.create(32, 32),
                anim_size=13
            ),
            Lifetime(self.conf.bomb_duration),
            Bomb(power)
        )
