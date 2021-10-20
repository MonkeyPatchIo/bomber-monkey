from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.player.input_mapping import InputMapping
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.game_inputs import GameInputs


class IAMapping(InputMapping):

    def __init__(self, ia: IA):
        super().__init__()
        self.ia = ia

    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        return PlayerAction.NONE
