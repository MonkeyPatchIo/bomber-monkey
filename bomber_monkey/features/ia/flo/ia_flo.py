from pathlib import Path

import numpy as np

from bomber_monkey.features.board.board import Board, Cell
from bomber_monkey.features.ia.flo.heatmap import Heatmap
from bomber_monkey.features.ia.flo.layer import Layer
from bomber_monkey.features.ia.flo.model import build_model, Features
from bomber_monkey.features.ia.flo.utils import choose
from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction

LAYERS = [
    Layer.Empty,
    Layer.Block,
    Layer.Wall,
    Layer.Bomb,
    Layer.Banana,
    Layer.Enemy,
]


def normalize(data: np.ndarray):
    a, b = data.min(), data.max()
    if a == b:
        return data
    return (data - a) / (b - a)


def debug(frame: int, features: Features):
    import cv2
    export = Path('/tmp/features')
    export.mkdir(parents=True, exist_ok=True)

    mapping = {
        'threat': features.threat,
        'attractiveness': features.attractiveness,
        'bomb_it': features.bomb_it,
        'path_finder': features.path_finder,
    }
    for name, data in mapping.items():
        data = normalize(data)
        zoom = 20
        data = np.kron(data, np.ones((zoom, zoom)))

        full_path = str(export / f'{name}_{frame}.png')
        cv2.imwrite(full_path, data * 255)


class FloIA(IA):
    def __init__(self):
        super().__init__()
        self.heatmap = Heatmap(layers=LAYERS)
        self.model = build_model(layers=LAYERS)
        self.frame = 0

    def get_action(self, board: Board, body: RigidBody) -> PlayerAction:
        player: Player = body.entity().get(Player)
        cell: Cell = board.by_pixel(body.pos)
        self.heatmap.load_board(board, player)

        heatmap = self.heatmap.heatmap
        features = self.model(heatmap)

        if self.frame % 10 == 0:
            debug(self.frame, features)
        self.frame += 1

        run_away = choose(cell, - features.threat)
        if run_away is not None:
            return run_away

        pick_item = choose(cell, features.attractiveness)
        if pick_item is not None:
            return pick_item

        bomb_it = choose(cell, features.bomb_it)
        if bomb_it == PlayerAction.NONE:
            self.cpt += 1
            return PlayerAction.MAIN_ACTION
        return bomb_it
