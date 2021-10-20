import pygame

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.controller.input_mapping import InputMapping
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.features.controller.mappings.utils import compute_action
from bomber_monkey.game_inputs import GameInputs
from python_ecs.ecs import Simulator


class JoystickMapping(InputMapping):
    def __init__(self, joystick_id: int):
        super().__init__()
        self.joystick_id = joystick_id
        self.move_actions = {
            pygame.K_LEFT: PlayerAction.MOVE_LEFT,
            pygame.K_RIGHT: PlayerAction.MOVE_RIGHT,
            pygame.K_UP: PlayerAction.MOVE_UP,
            pygame.K_DOWN: PlayerAction.MOVE_DOWN
        }
        self.tool_actions = {
            pygame.K_RETURN: PlayerAction.MAIN_ACTION,
            pygame.K_ESCAPE: PlayerAction.CANCEL,
        }

    def get_action(self, inputs: GameInputs, menu: bool, sim: Simulator = None, body: RigidBody = None) -> PlayerAction:
        return compute_action(
            self.move_actions,
            self.tool_actions,
            inputs.joysticks[self.joystick_id],
            menu
        )
