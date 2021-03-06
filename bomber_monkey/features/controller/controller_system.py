from bomber_monkey.features.board.board import Board
from bomber_monkey.features.controller.input_mapping import InputMapping
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import apply_action, PlayerAction
from bomber_monkey.game_inputs import get_game_inputs
from python_ecs.ecs import System, Simulator


class ControllerSystem(System):

    def __init__(self):
        super().__init__([RigidBody, InputMapping])

    def reverse_action(self, action: PlayerAction):
        if action == PlayerAction.MOVE_UP:
            return PlayerAction.MOVE_DOWN
        if action == PlayerAction.MOVE_DOWN:
            return PlayerAction.MOVE_UP
        if action == PlayerAction.MOVE_RIGHT:
            return PlayerAction.MOVE_LEFT
        if action == PlayerAction.MOVE_LEFT:
            return PlayerAction.MOVE_RIGHT
        return action

    def update(self, sim: Simulator, dt: float, body: RigidBody, input_mapping: InputMapping):
        if sim.context.game_elapsed_time < sim.context.conf.game_startup_delay:
            return
        lifetime: Lifetime = body.entity().get(Lifetime)
        if lifetime is not None and lifetime.is_expiring():
            return

        # update board state
        board: Board = sim.context.board
        if board.state.last_update < sim.last_update:
            board.state.update(sim)

        action = input_mapping.get_action(get_game_inputs(), menu=False, sim=sim, body=body)
        if input_mapping.reversed:
            action = self.reverse_action(action)

        apply_action(sim, action, body)
