import numpy as np

from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.board.board_state import BoardState
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.timing import timing

UNSET_VALUE = 0
SET_VALUE = 1


class Heatmap:
    def __init__(self):
        self.layers = [
            'Empty',
            'Block',
            'Wall',
            'Bomb',
            'Explosion',
            'Banana',
            'Enemy'
        ]
        self.depth = len(self.layers)
        self.heatmap: np.ndarray = None

    def load_board(self, board: Board, current_player: Player):
        with timing('Heatmap.load_board'):
            if self.heatmap is None:
                self.heatmap = UNSET_VALUE * np.ones((self.depth, board.width, board.height))
            else:
                self.heatmap.fill(UNSET_VALUE)

            state = board.state
            self._load_empty(board)
            self._load_blocks(board)
            self._load_walls(board)
            self._load_bombs(state)
            self._load_explosions(state)
            self._load_bananas(state)
            self._load_enemies(state, current_player)

            return self.heatmap

    def _load_empty(self, board: Board):
        for x in range(board.width):
            for y in range(board.height):
                if board.tile_grid[x, y] == Tiles.EMPTY:
                    self.heatmap[0, x, y] = SET_VALUE

    def _load_blocks(self, board: Board):
        for x in range(board.width):
            for y in range(board.height):
                if board.tile_grid[x, y] == Tiles.BLOCK:
                    self.heatmap[1, x, y] = SET_VALUE

    def _load_walls(self, board: Board):
        for x in range(board.width):
            for y in range(board.height):
                if board.tile_grid[x, y] == Tiles.WALL:
                    self.heatmap[2][x, y] = SET_VALUE

    def _load_bombs(self, state: BoardState):
        for (vec, item) in state.bombs.values():
            self.heatmap[3][vec.x, vec.y] = SET_VALUE

    def _load_explosions(self, state: BoardState):
        for (vec, item) in state.explosions.values():
            self.heatmap[4][vec.x, vec.y] = SET_VALUE

    def _load_bananas(self, state: BoardState):
        for (vec, item) in state.bananas.values():
            self.heatmap[5][vec.x, vec.y] = SET_VALUE

    def _load_enemies(self, state: BoardState, current_player: Player):
        for (vec, item) in state.players.values():
            if item != current_player:
                self.heatmap[6][vec.x, vec.y] = SET_VALUE
