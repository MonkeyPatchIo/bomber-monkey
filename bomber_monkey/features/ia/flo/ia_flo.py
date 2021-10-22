from bomber_monkey.features.board.board import Board, Cell
from bomber_monkey.features.ia.flo.heatmap import Heatmap
from bomber_monkey.features.ia.flo.layers.board_layer import BoardLayer
from bomber_monkey.features.ia.flo.layers.feature import Feature
from bomber_monkey.features.ia.flo.model import build_model
from bomber_monkey.features.ia.flo.utils import choose
from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction

LAYERS = [
    BoardLayer.Empty,
    BoardLayer.Block,
    BoardLayer.Wall,
    BoardLayer.Bomb,
    BoardLayer.Banana,
    BoardLayer.Enemy,
]


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

        self.frame += 1

        run_away = choose(cell, - features.get(Feature.Threat))
        if run_away is not None:
            features.debug('run_away', self.frame)
            return run_away

        pick_item = choose(cell, features.get(Feature.PickupTarget))
        if pick_item is not None:
            features.debug('pick_item', self.frame)
            return pick_item

        bomb_it = choose(cell, features.get(Feature.BombTarget))
        if bomb_it == PlayerAction.NONE:
            features.debug('bomb_it', self.frame)
            return PlayerAction.MAIN_ACTION
        return bomb_it
