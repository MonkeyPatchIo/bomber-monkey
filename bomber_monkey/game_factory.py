import random

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.board.board import Tiles, Board, random_blocks, clear_corners, wall_grid, fill_border, \
    clear_center
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.destruction.destruction import Destruction, Protection
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_controller import PlayerController
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.features.spawner.spawner import Spawner
from bomber_monkey.features.tile.tile_killer import TileKiller
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator


class GameFactory(object):

    @staticmethod
    def create_player(sim: Simulator, slot: PlayerSlot, controller: PlayerController):
        conf: GameConfig = sim.context.conf
        pos = slot.start_pos * conf.tile_size + conf.tile_size // 2

        sprite_size = Vector.create(40, 36)
        sprite = Sprite(
            image_id=slot.player_id,
            path=conf.media_path('monkey_sprite.png'),
            size=conf.tile_size,
            sprite_size=sprite_size,
            anim_size=10,
            offset=Vector.create(-4, -7)
        )
        sprite.change_color(conf.image_loader, slot.color)

        return sim.create(
            RigidBody(
                pos=pos,
                shape=Shape(Vector.create(36, 52)),
            ),
            sprite,
            Player(slot, conf.bomb_power),
            Spawner(conf.bomb_drop_rate, lambda body: GameFactory.create_bomb(sim, body)),
            controller
        )

    @staticmethod
    def create_explosion(sim: Simulator, pos: Vector):
        conf: GameConfig = sim.context.conf
        return sim.create(
            RigidBody(
                pos=pos,
                shape=Shape(conf.tile_size // 2),
            ),
            Image(
                conf.media_path('fire.png'),
                size=conf.tile_size // 2,
            ),
            Lifetime(conf.explosion_duration),
            Destruction(),
            TileKiller(Tiles.BLOCK)
        )

    @staticmethod
    def create_board(sim: Simulator):
        conf: GameConfig = sim.context.conf

        board = Board(tile_size=conf.tile_size, grid_size=conf.grid_size)
        sim.on_create.append(board.on_create)
        sim.on_destroy.append(board.on_destroy)

        random_blocks(board, Tiles.BLOCK, 1.)
        # random_blocks(board, Tiles.WALL, .5)
        clear_corners(board)
        clear_center(board)

        wall_grid(board)

        fill_border(board, Tiles.WALL)
        sim.create(board)

        return board

    @staticmethod
    def create_banana(sim: Simulator, body: RigidBody, probability: float = 1):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        if random.random() > probability:
            return None

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Sprite(
                conf.media_path('banana_sprite32.png'),
                size=conf.tile_size,
                sprite_size=Vector.create(32, 32),
                anim_size=11,
                anim_time=.5
            ),
            Banana(),
            Protection(duration=conf.explosion_duration * 2)
        )

    @staticmethod
    def create_bomb(sim: Simulator, body: RigidBody):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        player: Player = body.entity().get(Player)
        power = player.power if player else conf.bomb_power

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Sprite(
                conf.media_path('bomb_sprite.png'),
                size=conf.tile_size * 2,
                sprite_size=Vector.create(32, 32),
                anim_size=13
            ),
            Lifetime(conf.bomb_duration),
            Bomb(power)
        )
