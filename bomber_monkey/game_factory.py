import random
from typing import Optional

import numpy as np

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.board.board import Tiles, Board, random_blocks, clear_corners, wall_grid, fill_border, \
    clear_center
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.destruction.destruction import Destruction, Protection
from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.display.sprite_animation import switch_anim, union_anim, loop_anim, \
    sequence_anim, static_anim, single_anim, flip_anim, rotate_anim, stateful_condition
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

EPSILON = 0.1


class GameFactory(object):

    @staticmethod
    def create_player(sim: Simulator, slot: PlayerSlot, controller: PlayerController):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board
        pos = board.by_relative_grid(slot.start_pos).center

        def moving_right(body: RigidBody) -> Optional[bool]:
            if body.speed.x > EPSILON:
                return True
            if body.speed.x < -EPSILON:
                return False
            return None

        sprite = Sprite(
            path=conf.media_path('monkey_sprite.png'),
            nb_images=10,
            animation=union_anim([
                switch_anim([
                    (
                        lambda body: np.linalg.norm(body.speed.data) > EPSILON,  # running
                        loop_anim(0.02)
                    ),
                    (
                        lambda body: body.entity().get(Lifetime).is_expiring(),  # dying
                        sequence_anim(0.2, [
                            flip_anim(True),
                            flip_anim(False),
                        ])
                    )
                    ],
                    static_anim()
                ),
                stateful_condition(moving_right, flip_anim(True))
            ]),
            display_size=conf.tile_size,
            offset=Vector.create(-4, -7),
            color_tint=slot.color,
            layer=1
        )

        return sim.create(
            RigidBody(
                pos=pos,
                shape=Shape(Vector.create(36, 52)),
            ),
            sprite,
            Player(slot, conf.bomb_power),
            Lifetime(conf.player_death_duration, delayed=True),
            Spawner(conf.bomb_drop_rate, lambda body: GameFactory.create_bomb(sim, body)),
            controller
        )

    @staticmethod
    def create_explosion(sim: Simulator, pos: Vector, direction: ExplosionDirection, power: int):
        conf: GameConfig = sim.context.conf

        rotation = 0
        png = 'fire_end.png' if power > 0 else 'fire_middle.png'
        nb_images = 8 if power > 0 else 6
        if direction == ExplosionDirection.LEFT:
            rotation = 90
        elif direction == ExplosionDirection.DOWN:
            rotation = 180
        elif direction == ExplosionDirection.RIGHT:
            rotation = -90
        elif direction != ExplosionDirection.UP:
            png = 'fire_center.png'
            nb_images = 6

        return sim.create(
            RigidBody(
                pos=pos,
                shape=Shape(conf.tile_size),
            ),
            Sprite(
                conf.media_path(png),
                nb_images=nb_images,
                animation=union_anim([
                    loop_anim(image_per_sec=conf.bomb_explosion_propagation_time / 2, intro_length=2,
                              outro_length=2, total_duration=conf.explosion_duration),
                    rotate_anim(rotation)
                ]),
                display_size=conf.tile_size
            ),
            Explosion(direction, power),
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
                nb_images=11,
                animation=loop_anim(0.1),
                display_size=Vector.create(52, 52),
                layer=1
            ),
            Banana(),
            Protection(duration=conf.explosion_duration * 2)
        )

    @staticmethod
    def create_bomb(sim: Simulator, body: RigidBody):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        cell = board.by_pixel(body.pos)
        if cell.has_bomb:
            return

        player: Player = body.entity().get(Player)
        power = player.power if player else conf.bomb_power

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Sprite(
                conf.media_path('bomb_sprite.png'),
                nb_images=10,
                animation=single_anim(conf.bomb_duration),
                display_size=Vector.create(int(conf.tile_size.x * 1.5), int(conf.tile_size.y * 1.5))
            ),
            Lifetime(conf.bomb_duration),
            Bomb(power)
        )
