from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.game_inputs import GameInputs
from python_ecs.ecs import Component


class InputMapping(Component):
    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        pass