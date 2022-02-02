import random

from bomber_monkey.features.board.board import Tiles, Board, fill_board, Cell
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.controller.input_mapping import InputMapping
from bomber_monkey.features.destruction.destruction import Destruction, Protection, Destructible
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.display.sprite import Sprite, SpriteSet
from bomber_monkey.features.display.sprite_animation import LoopAnim, RotateAnim, SingleAnim, FlipAnim, UnionAnim, \
    SequenceAnim, StaticAnim, ShakingAnim
from bomber_monkey.features.items.banana import Banana
from bomber_monkey.features.items.immunity import ImmunityItem
from bomber_monkey.features.items.reverse_control import ReserveControlItem
from bomber_monkey.features.items.speed_down import SpeedDownItem
from bomber_monkey.features.items.speed_up import SpeedUpItem
from bomber_monkey.features.items.stronger import StrongerItem
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_animator import DEFAULT_PLAYER_SIZE
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.features.spawner.spawner import Spawner
from bomber_monkey.features.tile.tile_killer import TileKiller
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator


class GameFactory(object):

    @staticmethod
    def create_player(sim: Simulator, slot: PlayerSlot, input_mapping: InputMapping):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board
        pos = board.by_relative_grid(slot.start_pos).center

        player_sprite = Sprite(
            name="player",
            path=conf.media_path('monkey_sprite.png'),
            nb_images=10,
            animation=UnionAnim([
                SequenceAnim(0.2, [
                    FlipAnim(True),
                    FlipAnim(False),
                ], name="dying", enabled=False),
                LoopAnim(0.02, name="running", enabled=False),
                StaticAnim(name="static", enabled=False),
                FlipAnim(True, name="moving_right", enabled=False)
            ]),
            display_size=Vector.create(DEFAULT_PLAYER_SIZE, DEFAULT_PLAYER_SIZE),
            offset=Vector.create(-4, -7),
            color_tint=slot.color,
            layer=1
        )
        rain_sprite = Sprite(
            name="rain",
            display=False,
            path=conf.media_path('rain_sprite.png'),
            nb_images=10,
            animation=UnionAnim([
                LoopAnim(0.1),
                FlipAnim(True, name="moving_right", enabled=False)
            ]),
            display_size=conf.tile_size,
            offset=Vector.create(-4, -7),
            layer=1
        )
        php_sprite = Sprite(
            name="php",
            display=False,
            path=conf.media_path('php_sprite.png'),
            nb_images=10,
            animation=UnionAnim([
                LoopAnim(0.1),
                FlipAnim(True, name="moving_right", enabled=False)
            ]),
            display_size=conf.tile_size,
            offset=Vector.create(-4, -7),
            layer=1
        )

        return sim.create(
            RigidBody(
                pos=pos,
                shape=Shape(Vector.create(36, 52)),
            ),
            SpriteSet([php_sprite, player_sprite, rain_sprite]),
            Destructible(),
            Player(slot, conf.bomb_power),
            Protection(0),
            Lifetime(conf.player_death_duration, delayed_ttl=True),
            Spawner(conf.bomb_drop_rate, lambda body: GameFactory.create_bomb(sim, body)),
            input_mapping
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
                animation=UnionAnim([
                    LoopAnim(image_per_sec=conf.bomb_explosion_propagation_time / 2, intro_length=2,
                             outro_length=2, total_duration=conf.explosion_duration),
                    RotateAnim(rotation)
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
        fill_board(board)
        sim.create(board)

        return board

    @staticmethod
    def create_item(sim: Simulator, body: RigidBody):
        mapping = {
            'None': lambda sim, body: None,
            'Banana': GameFactory.create_banana,
            'PhpItem': GameFactory.create_php,
            'RustItem': GameFactory.create_rust,
            'JavaItem': GameFactory.create_java,
            'Html5Item': GameFactory.create_html5,
        }

        conf: GameConfig = sim.context.conf
        r = random.random() * sum(conf.item_rates.values())
        for kind, rate in conf.item_rates.items():
            if r < rate:
                factory = mapping[kind]
                factory(sim, body)
                return
            r -= rate

    @staticmethod
    def create_banana(sim: Simulator, body: RigidBody):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Sprite(
                conf.media_path('banana_sprite32.png'),
                nb_images=11,
                animation=LoopAnim(0.1),
                display_size=Vector.create(52, 52),
                layer=1
            ),
            Banana(),
            Destructible(),
            Protection(duration=conf.explosion_duration * 2)
        )

    @staticmethod
    def create_php(sim: Simulator, body: RigidBody):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Image(
                conf.media_path('php.png'),
                display_size=Vector.create(40, 40)
            ),
            ImmunityItem(),
            Destructible(),
            Protection(duration=conf.explosion_duration * 2)
        )

    @staticmethod
    def create_rust(sim: Simulator, body: RigidBody):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Image(
                conf.media_path('rust.png'),
                display_size=Vector.create(40, 40)
            ),
            SpeedUpItem(),
            Destructible(),
            Protection(duration=conf.explosion_duration * 2)
        )

    @staticmethod
    def create_java(sim: Simulator, body: RigidBody):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Image(
                conf.media_path('java.png'),
                display_size=Vector.create(40, 40)
            ),
            SpeedDownItem(),
            StrongerItem(),
            Destructible(),
            Protection(duration=conf.explosion_duration * 2)
        )

    @staticmethod
    def create_html5(sim: Simulator, body: RigidBody):
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        return sim.create(
            RigidBody(
                pos=board.by_pixel(body.pos).center,
                shape=Shape(conf.tile_size),
            ),
            Image(
                conf.media_path('html5.png'),
                display_size=Vector.create(40, 40)
            ),
            ReserveControlItem(),
            Destructible(),
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
                animation=SingleAnim(conf.bomb_duration),
                display_size=Vector.create(int(conf.tile_size.x * 1.5), int(conf.tile_size.y * 1.5))
            ),
            Lifetime(conf.bomb_duration),
            Bomb(power)
        )

    @staticmethod
    def create_shaking_block(sim: Simulator, cell: Cell):
        conf: GameConfig = sim.context.conf
        return sim.create(
            RigidBody(
                pos=cell.center,
                shape=Shape(conf.tile_size)
            ),
            Sprite(
                name="block",
                path=conf.media_path('tiles/jungle_block.png'),
                nb_images=1,
                animation=ShakingAnim(conf.block_shaking_duration, conf.block_shaking_size,
                                      name="shaking", enabled=True),
                display_size=conf.tile_size
            ),
            Destructible()
        )
