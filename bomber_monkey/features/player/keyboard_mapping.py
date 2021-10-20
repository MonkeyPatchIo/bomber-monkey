from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.features.player.user_input_mapping import UserInputMapping, compute_action
from bomber_monkey.game_inputs import GameInputs

PygameKey = int


class KeyboardMapping(UserInputMapping):
    def __init__(self,
                 left_key: PygameKey,
                 right_key: PygameKey,
                 up_key: PygameKey,
                 down_key: PygameKey,
                 action_key: PygameKey,
                 cancel_key: PygameKey
                 ):
        super().__init__()
        self.move_actions = {
            left_key: PlayerAction.MOVE_LEFT,
            right_key: PlayerAction.MOVE_RIGHT,
            up_key: PlayerAction.MOVE_UP,
            down_key: PlayerAction.MOVE_DOWN
        }
        self.tool_actions = {
            action_key: PlayerAction.MAIN_ACTION,
            cancel_key: PlayerAction.CANCEL,
        }

    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        return compute_action(
            self.move_actions,
            self.tool_actions,
            inputs.keyboard,
            menu
        )
