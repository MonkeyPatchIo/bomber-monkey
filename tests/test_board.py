from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Entity


def create_board():
    return Board(
        grid_size=Vector.create(8, 8),
        tile_size=Vector.create(32, 32)
    )


def test_set():
    board = create_board()
    for x in range(board.width):
        for y in range(board.height):
            for tile in list(Tiles):
                board.by_grid(Vector.create(x, y)).tile = tile
                assert board.by_grid(Vector.create(x, y)).tile == tile


def test_cell_set_tile():
    board = create_board()
    actual = board.by_grid(Vector.create(1, 1))
    assert actual.tile == Tiles.EMPTY

    actual.tile = Tiles.BLOCK
    assert actual.tile == Tiles.BLOCK

    expected = board.by_grid(Vector.create(1, 1))
    assert expected.tile == Tiles.BLOCK

    actual.tile = Tiles.EMPTY
    assert actual.tile == Tiles.EMPTY

    expected = board.by_grid(Vector.create(1, 1))
    assert expected.tile == Tiles.EMPTY


def test_get_by_grid():
    board = create_board()
    assert board.by_grid(Vector.create(board.width, 0)) is None
    assert board.by_grid(Vector.create(0, board.height)) is None
    assert board.by_grid(Vector.create(0, -1)) is None
    assert board.by_grid(Vector.create(-1, 0)) is None


def test_get_by_pixel():
    board = create_board()
    cell = board.by_pixel(Vector.create(0, 0))
    assert cell is not None
    assert cell.grid == Vector.create(0, 0)

    cell = board.by_pixel(Vector.create(32, 64))
    assert cell is not None
    assert cell.grid == Vector.create(1, 2)

    cell = board.by_pixel(Vector.create(31, 63))
    assert cell is not None
    assert cell.grid == Vector.create(0, 1)

    assert board.by_pixel(Vector.create(-1, 0)) is None
    assert board.by_pixel(Vector.create(0, -1)) is None
    assert board.by_pixel(Vector.create(8 * 32, 0)) is None
    assert board.by_pixel(Vector.create(0, 8 * 32)) is None


def test_move():
    board = create_board()
    cell_origin = board.by_grid(Vector.create(0, 0))
    assert cell_origin is not None
    assert cell_origin.left() is None
    assert cell_origin.up() is None
    assert cell_origin.right().grid == Vector.create(1, 0)
    assert cell_origin.down().grid == Vector.create(0, 1)

    cell_max = board.by_grid(Vector.create(board.width - 1, board.height - 1))
    assert cell_max is not None
    assert cell_max.right() is None
    assert cell_max.down() is None
    assert cell_max.left().grid == Vector.create(board.width - 2, board.height - 1)
    assert cell_max.up().grid == Vector.create(board.width - 1, board.height - 2)

    cell = cell_origin.move(Vector.create(0, 0))
    assert cell.grid == Vector.create(0, 0)
    cell = cell_origin.move(Vector.create(1, 1))
    assert cell.grid == Vector.create(1, 1)
    assert cell_origin.move(Vector.create(-1, 0)) is None
    assert cell_origin.move(Vector.create(0, -1)) is None
    assert cell_max.move(Vector.create(1, 0)) is None
    assert cell_max.move(Vector.create(0, 1)) is None


def test_bomb():
    board = create_board()
    cell = board.by_grid(Vector.create(0, 0))
    assert not cell.has_bomb

    cell.bomb = Entity(None, 0)
    cell = board.by_grid(Vector.create(0, 0))
    assert cell is not None

    cell.bomb = None
    cell = board.by_grid(Vector.create(0, 0))
    assert not cell.has_bomb


def test_pixel():
    board = create_board()
    cell = board.by_grid(Vector.create(0, 0))
    assert cell.top_left == Vector.create(0, 0)
    assert cell.center == Vector.create(16, 16)

    cell = board.by_grid(Vector.create(2, 3))
    assert cell.top_left == Vector.create(64, 96)
    assert cell.center == Vector.create(80, 112)

