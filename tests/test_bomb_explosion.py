from bomber_monkey.game_config import GameConfig
from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.systems.entity_factory import EntityBuilder
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.states.game_state import GameState
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import sim


class DummyAvatar:
    def __init__(self, pos):
        self.body = RigidBody(pos=pos)
        self.dropper = EntityBuilder(drop_rate=0)

    def get(self, component):
        if component == RigidBody:
            return self.body
        if component == EntityBuilder:
            return self.dropper
        raise 'DummyAvatar: Unsupported component type "{}"'.format(component)


class Init:
    def __init__(self, blocks=[], bombs=[(2, 2, True)]):
        self.bombs = bombs
        self.blocks = blocks


def assert_system_update(init: Init, expected_tiles):
    conf: GameConfig = GameConfig()
    conf.bomb_duration = 999999999  # Pseudo-infinite
    conf.bomb_power = 2
    board: Board = Board(tile_size=conf.tile_size, grid_size=conf.grid_size)
    state: GameState = GameState(conf, board)
    bomb_explosion_system = BombExplosionSystem(state)
    wall_explosion_system = TileKillerSystem(board)

    sim.reset()
    sim.reset_systems([
        bomb_explosion_system,
        wall_explosion_system
    ])
    sim.on_create.append(board.on_create)
    sim.on_destroy.append(board.on_destroy)

    for (x, y) in init.blocks:
        board.by_grid(Vector.create(x, y)).tile = Tiles.BLOCK

    for (x, y, expire) in init.bombs:
        cell = board.by_grid(Vector.create(x, y))
        bomb = state.create_bomb(RigidBody(pos=cell.center), 2)
        if expire:
            life: Lifetime = bomb.get(Lifetime)
            life.expire()

    sim.update()

    for (x, y, expected) in expected_tiles:
        actual = board.by_grid(Vector.create(x, y)).tile
        assert actual == expected, '{},{} -> {}   ==   {}'.format(x, y, actual, expected)


def test_empty_grid():
    init = Init()

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_top_block():
    init = Init(blocks=[
        (2, 0),
        (2, 1)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.BLOCK),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_top_two_block():
    init = Init(blocks=[
        (2, 0)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_right_block():
    init = Init(blocks=[
        (3, 2),
        (4, 2)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.BLOCK),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_bottom_block():
    init = Init(blocks=[
        (2, 3),
        (2, 4)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.BLOCK)
    ]

    assert_system_update(init, expecteds)


def test_left_block():
    init = Init(blocks=[
        (0, 2),
        (1, 2)
    ])

    expecteds = [
        (0, 2, Tiles.BLOCK),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_bomb_chain_two():
    init = Init(
        blocks=[
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (3, 2), (4, 2),
            (0, 3), (1, 3), (3, 3), (4, 3),
            (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5),
        ],
        bombs=[
            (2, 2, True),
            (2, 3, False),
        ]
    )

    expecteds = [
        (0, 0, Tiles.BLOCK), (1, 0, Tiles.BLOCK), (2, 0, Tiles.BLOCK), (3, 0, Tiles.BLOCK), (4, 0, Tiles.BLOCK),
        (0, 1, Tiles.BLOCK), (1, 1, Tiles.BLOCK), (2, 1, Tiles.EMPTY), (3, 1, Tiles.BLOCK), (4, 1, Tiles.BLOCK),
        (0, 2, Tiles.BLOCK), (1, 2, Tiles.EMPTY), (2, 2, Tiles.EMPTY), (3, 2, Tiles.EMPTY), (4, 2, Tiles.BLOCK),
        (0, 3, Tiles.BLOCK), (1, 3, Tiles.EMPTY), (2, 3, Tiles.EMPTY), (3, 3, Tiles.EMPTY), (4, 3, Tiles.BLOCK),
        (0, 4, Tiles.BLOCK), (1, 4, Tiles.BLOCK), (2, 4, Tiles.EMPTY), (3, 4, Tiles.BLOCK), (4, 4, Tiles.BLOCK),
        (0, 5, Tiles.BLOCK), (1, 5, Tiles.BLOCK), (2, 5, Tiles.BLOCK), (3, 5, Tiles.BLOCK), (4, 5, Tiles.BLOCK),
    ]

    assert_system_update(init, expecteds)
