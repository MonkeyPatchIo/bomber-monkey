from typing import List, Tuple

from bomber_monkey.features.board.board import Tiles, Board
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem, ExplosionPropagationSystem
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator, Entity

board_size = Vector.create(5, 5)
tile_size = Vector.create(10, 10)
empty_middle_lines = [(x, board_size.x // 2, Tiles.EMPTY) for x in range(0, board_size.x)]\
                     + [(board_size.y // 2, y, Tiles.EMPTY) for y in range(0, board_size.y)]


class Context(object):
    def __init__(self, conf: GameConfig, board: Board):
        self.conf = conf
        self.board = board


class Init:
    def __init__(self, blocks=None, bombs=None):
        self.bombs = bombs or [(2, 2, True)]
        self.blocks = blocks or []


def create_env():
    conf: GameConfig = GameConfig()
    conf.bomb_duration = 999999999  # Pseudo-infinite
    conf.bomb_explosion_propagation_time = 0
    conf.bomb_power = 2
    board = Board(
        board_size,
        tile_size
    )
    sim = Simulator(Context(conf, board))
    sim.reset_systems([
        BombExplosionSystem(),
        ExplosionPropagationSystem(),
        TileKillerSystem(),
    ])
    return board, sim


def plant_bomb(board: Board, sim: Simulator, x: int, y: int):
    cell = board.by_grid(Vector.create(x, y))
    body = RigidBody(pos=cell.center)
    sim.create(body)
    sim.update()  # create body
    bomb = GameFactory.create_bomb(sim, body)
    sim.update()  # create bomb
    return bomb


def explode_bomb(bomb: Entity, sim: Simulator):
    life: Lifetime = bomb.get(Lifetime)
    life.expire()
    sim.update()


def change_expected(expected_tiles, new_expected_tile):
    return [
        expected_tile
        for expected_tile in expected_tiles
        if expected_tile[0] != new_expected_tile[0] or expected_tile[1] != new_expected_tile[1]
    ] + [new_expected_tile]


def assert_middle_lines(board: Board, blocks: List[Tuple[int, int]]):
    expected_tiles = empty_middle_lines.copy()
    for (x, y) in blocks:
        expected_tiles = change_expected(expected_tiles, (x, y, Tiles.BLOCK))
    assert_board(board, expected_tiles)


def assert_board(board: Board, expected_tiles):
    for (x, y, expected) in expected_tiles:
        actual = board.by_grid(Vector.create(x, y)).tile
        assert actual == expected, 'At ({},{}), expecting {} but got {}'.format(x, y, expected, actual)


def test_empty_grid():
    board, sim = create_env()
    bomb = plant_bomb(board, sim, 2, 2)
    explode_bomb(bomb, sim)
    assert_board(board, empty_middle_lines)


def test_top_block():
    board, sim = create_env()
    board.by_grid(Vector.create(2, 0)).tile = Tiles.BLOCK
    board.by_grid(Vector.create(2, 1)).tile = Tiles.BLOCK
    bomb = plant_bomb(board, sim, 2, 2)
    explode_bomb(bomb, sim)
    assert_middle_lines(board, [(2, 0), (2, 1)])
    sim.update()  # fire propagates next cells
    assert_middle_lines(board, [(2, 0), (2, 1)])
    sim.update()  # fire destroy cell, propagate next cells
    assert_middle_lines(board, [(2, 0)])
    sim.update()  # fire stopped
    assert_middle_lines(board, [(2, 0)])


def test_top_two_block():
    board, sim = create_env()
    board.by_grid(Vector.create(2, 0)).tile = Tiles.BLOCK
    bomb = plant_bomb(board, sim, 2, 2)
    explode_bomb(bomb, sim)
    assert_middle_lines(board, [(2, 0)])
    sim.update()  # fire propagates next cells
    assert_middle_lines(board, [(2, 0)])
    sim.update()  # fire propagate next cells
    assert_middle_lines(board, [(2, 0)])
    sim.update()  # fire destroy cell
    assert_board(board, empty_middle_lines)


def test_right_block():
    board, sim = create_env()
    board.by_grid(Vector.create(3, 2)).tile = Tiles.BLOCK
    board.by_grid(Vector.create(4, 2)).tile = Tiles.BLOCK
    bomb = plant_bomb(board, sim, 2, 2)
    explode_bomb(bomb, sim)
    assert_middle_lines(board, [(3, 2), (4, 2)])
    sim.update()  # fire propagates next cells
    assert_middle_lines(board, [(3, 2), (4, 2)])
    sim.update()  # fire destroy cell, propagate next cells
    assert_middle_lines(board, [(4, 2)])
    sim.update()  # fire stopped
    assert_middle_lines(board, [(4, 2)])


def test_bottom_block():
    board, sim = create_env()
    board.by_grid(Vector.create(2, 3)).tile = Tiles.BLOCK
    board.by_grid(Vector.create(2, 4)).tile = Tiles.BLOCK
    bomb = plant_bomb(board, sim, 2, 2)
    explode_bomb(bomb, sim)
    assert_middle_lines(board, [(2, 3), (2, 4)])
    sim.update()  # fire propagates next cells
    assert_middle_lines(board, [(2, 3), (2, 4)])
    sim.update()  # fire destroy cell, propagate next cells
    assert_middle_lines(board, [(2, 4)])
    sim.update()  # fire stopped
    assert_middle_lines(board, [(2, 4)])


def test_left_block():
    board, sim = create_env()
    board.by_grid(Vector.create(0, 2)).tile = Tiles.BLOCK
    board.by_grid(Vector.create(1, 2)).tile = Tiles.BLOCK
    bomb = plant_bomb(board, sim, 2, 2)
    explode_bomb(bomb, sim)
    assert_middle_lines(board, [(0, 2), (1, 2)])
    sim.update()  # fire propagates next cells
    assert_middle_lines(board, [(0, 2), (1, 2)])
    sim.update()  # fire destroy cell, propagate next cells
    assert_middle_lines(board, [(0, 2)])
    sim.update()  # fire stopped
    assert_middle_lines(board, [(0, 2)])


def test_bomb_chain_two():
    board, sim = create_env()
    expected_tiles = []

    for x in range(0, 5):
        for y in range(0, 5):
            if (x == 2 and y == 2) or (x == 2 and y == 3):
                board.by_grid(Vector.create(x, y)).tile = Tiles.EMPTY
                expected_tiles.append((x, y, Tiles.EMPTY))
            else:
                board.by_grid(Vector.create(x, y)).tile = Tiles.BLOCK
                expected_tiles.append((x, y, Tiles.BLOCK))

    bomb = plant_bomb(board, sim, 2, 2)
    plant_bomb(board, sim, 2, 3)
    explode_bomb(bomb, sim)
    assert_board(board, expected_tiles)
    sim.update()  # fire propagates next cells, explode the other bomb
    assert_board(board, expected_tiles)
    sim.update()  # fire destroy cells, bomb2 fire propagates next cells
    expected_tiles = change_expected(expected_tiles, (2, 1, Tiles.EMPTY))
    expected_tiles = change_expected(expected_tiles, (1, 2, Tiles.EMPTY))
    expected_tiles = change_expected(expected_tiles, (3, 2, Tiles.EMPTY))
    assert_board(board, expected_tiles)
    sim.update()  # bomb2 fire destroy cell
    expected_tiles = change_expected(expected_tiles, (2, 4, Tiles.EMPTY))
    assert_board(board, expected_tiles)
    sim.update()  # no more fire
    assert_board(board, expected_tiles)
