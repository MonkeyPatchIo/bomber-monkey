from bomber_monkey.features.board.board import Board, Cell
from bomber_monkey.features.ia.flo.heatmap import Heatmap
from bomber_monkey.features.ia.flo.model import build_model
from bomber_monkey.features.ia.flo.utils import choose, is_ignored
from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction


class FloIA(IA):
    def __init__(self):
        super().__init__()
        self.heatmap = Heatmap()
        self.model = build_model()

    def get_action(self, board: Board, body: RigidBody) -> PlayerAction:
        player: Player = body.entity().get(Player)
        cell: Cell = board.by_pixel(body.pos)
        self.heatmap.load_board(board, player)

        heatmap = self.heatmap.heatmap
        features = self.model(heatmap)

        best_move = choose(cell, - features.run_away)
        if best_move != PlayerAction.NONE:
            return best_move

        best_move = choose(cell, features.pick_item)
        if best_move != PlayerAction.NONE:
            return best_move

        best_move = choose(cell, features.bomb_it)
        if best_move == PlayerAction.NONE and is_ignored(features.run_away):
            return PlayerAction.MAIN_ACTION

        return best_move
