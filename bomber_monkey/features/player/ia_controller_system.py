from bomber_monkey.features.board.board import Board
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.ia import IAGaol, find_goal
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import InputMapping, PlayerAction, apply_action

from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_inputs import GameInputs
from python_ecs.ecs import System, Simulator


class IAMapping(InputMapping):

    def __init__(self, left_key, right_key):
        super().__init__()
        self.left_key = left_key
        self.right_key = right_key

    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        if self.left_key in inputs.keyboard.up:
            return PlayerAction.MOVE_LEFT
        if self.right_key in inputs.keyboard.up:
            return PlayerAction.MOVE_RIGHT
        return PlayerAction.NONE


class IAControllerSystem(System):

    def __init__(self):
        super().__init__([RigidBody, IAMapping])
        self.goal: IAGaol = IAGaol(PlayerAction.NONE, None)

    def update(self, sim: Simulator, dt: float, body: RigidBody, input_mapping: IAMapping):
        if sim.context.game_elapsed_time < sim.context.conf.game_startup_delay:
            return
        lifetime: Lifetime = body.entity().get(Lifetime)
        if lifetime is not None and lifetime.is_expiring():
            return
        player: Player = body.entity().get(Player)

        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        body_cell = board.by_pixel(body.pos)
        # if self.goal.destination is None or self.goal.destination == body_cell:
        new_goal = find_goal(body_cell, player)
        self.goal.action = new_goal.action
        self.goal.destination = new_goal.destination
        apply_action(sim, self.goal.action, body, conf)
