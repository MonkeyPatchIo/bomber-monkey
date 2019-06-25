from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.utils.vector import Vector

def assert_system_update(init, expecteds):
    conf = BomberGameConfig()
    board = Board(tile_size=conf.tile_size, grid_size=conf.grid_size)
    conf._board = board
    system = BombExplosionSystem(conf)

    for (x, y, tile) in init:
        board.by_grid(Vector.create(x, y)).tile = tile

    explosion = BombExplosion(2)
    body = RigidBody(pos=conf.tile_size * (2, 2))
    lifetime = Lifetime(0)
    system.update(explosion, body, lifetime)

    for (x, y, expected) in expecteds:
        actual = board.by_grid(Vector.create(x, y)).tile
        assert actual == expected, '{},{} -> {}   ==   {}'.format(x, y, actual, expected) 


def test_empty_grid():
    init = []

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
    init = [
        (2, 0, Tiles.TREE0),
        (2, 1, Tiles.TREE0)
    ]

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.TREE0),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_top_two_block():
    init = [
        (2, 0, Tiles.TREE0)
    ]

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
    init = [
        (3, 2, Tiles.TREE0),
        (4, 2, Tiles.TREE0)
    ]

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.TREE0),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_bottom_block():
    init = [
        (2, 3, Tiles.TREE0),
        (2, 4, Tiles.TREE0)
    ]

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
        (2, 4, Tiles.TREE0)
    ]

    assert_system_update(init, expecteds)


def test_left_block():
    init = [
        (0, 2, Tiles.TREE0),
        (1, 2, Tiles.TREE0)
    ]

    expecteds = [
        (0, 2, Tiles.TREE0),
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