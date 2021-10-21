from bomber_monkey.features.board.board import Board
from bomber_monkey.features.controller.input_mapping import InputMapping
from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.game_inputs import GameInputs
from bomber_monkey.utils.timing import timing
from python_ecs.ecs import Simulator


class IAMapping(InputMapping):
    def __init__(self, ia: IA):
        super().__init__()
        self.ia = ia

    def get_action(self, inputs: GameInputs, menu: bool, sim: Simulator = None, body: RigidBody = None) -> PlayerAction:
        with timing(f'ia.get_action : {self.ia.__class__.__name__}#{hash(self.ia)}'):
            board: Board = sim.context.board
            return self.ia.get_action(board, body)
