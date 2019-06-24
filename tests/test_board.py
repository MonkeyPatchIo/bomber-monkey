from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.utils.vector import Vector

board = Board(
    grid_size=Vector.create(8, 8),
    tile_size=Vector.create(32, 32)
)


def test_set():
    for x in range(board.width):
        for y in range(board.height):
            for tile in list(Tiles):
                board.set(3, 5, tile)
                assert board.get(3, 5) == tile
