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
from bomber_monkey.features.player.player_killer import PlayerKiller
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.features.systems.entity_factory import EntityBuilder
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

    @property
    def players(self) -> List[Entity]:
        return self.game_state.players

    def _on_destroy_player(self, entity: Entity):
        player: Player = entity.get(Player)
        if player:
            self.players.remove(entity)

    def create_player(self, slot: PlayerSlot, controller: PlayerController):

        pos = slot.start_pos * self.conf.tile_size + self.conf.tile_size // 2

        sprite = Sprite(
            image_id=slot.player_id,
            path='resources/monkey_sprite.png',
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
            EntityBuilder(self.conf.bomb_drop_rate, self.create_bomb),
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
                'resources/fire.png',
                size=self.conf.tile_size // 2,
            ),
            Lifetime(self.conf.explosion_duration),
            PlayerKiller(),
            TileKiller(Tiles.BLOCK)
        )

    def create_board(self):
        board = Board(tile_size=self.conf.tile_size, grid_size=self.conf.grid_size)
        self.sim.on_create.append(board.on_create)
        self.sim.on_destroy.append(board.on_destroy)
        self.sim.on_destroy.append(self._on_destroy_player)

        random_blocks(board, Tiles.BLOCK, 1.)
        # random_blocks(board, Tiles.WALL, .5)
        clear_corners(board)
        clear_center(board)

        wall_grid(board)

        fill_border(board, Tiles.WALL)
        self.game_state._board = board

        return self.sim.create(board)

    def create_banana(self, body: RigidBody, probability: float = 1):
        if random.random() > probability:
            return None

        return self.sim.create(
            RigidBody(
                pos=self.board.by_pixel(body.pos).center,
                shape=Shape(self.conf.tile_size),
            ),
            Sprite(
                'resources/banana_sprite32.png',
                size=self.conf.tile_size,
                sprite_size=Vector.create(32, 32),
                anim_size=11,
                anim_time=.5
            ),
            Banana()
        )

    def create_bomb(self, body: RigidBody):
        entity = self.sim.get(body.eid)
        player: Player = entity.get(Player)

        return self.sim.create(
            RigidBody(
                pos=self.board.by_pixel(body.pos).center,
                shape=Shape(self.conf.tile_size),
            ),
            Sprite(
                'resources/bomb_sprite.png',
                size=self.conf.tile_size * 2,
                sprite_size=Vector.create(32, 32),
                anim_size=13
            ),
            Lifetime(self.conf.bomb_duration),
            Bomb(player.power)
        )
