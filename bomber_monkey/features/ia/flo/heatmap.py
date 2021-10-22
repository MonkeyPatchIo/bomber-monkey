from typing import List

import numpy as np

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.ia.flo.layer import Layer
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.timing import timing

UNSET_VALUE = 0

DEFAULT_LAYERS = [
    Layer.Empty,
    Layer.Block,
    Layer.Bomb,
    Layer.Banana,
    Layer.Enemy,
    Layer.Explosion,
]


class Heatmap:
    def __init__(self, layers: List[Layer] = None):
        self.layers = layers or DEFAULT_LAYERS
        self.heatmap: np.ndarray = None

    def load_board(self, board: Board, current_player: Player):
        with timing('Heatmap.load_board'):
            self.init_buffer(board)

            for i, layer in enumerate(self.layers):
                loader = layer.get_loader()
                loader(self.heatmap, i, board, current_player)

            return self.heatmap

    def init_buffer(self, board: Board):
        depth = len(self.layers)
        if self.heatmap is None:
            self.heatmap = UNSET_VALUE * np.ones((depth, board.height, board.width))
        else:
            self.heatmap.fill(UNSET_VALUE)
