import functools
from typing import Dict

from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.game_inputs import ControllerInputs


def compute_action(
        move_actions: Dict[int, PlayerAction],
        tool_actions: Dict[int, PlayerAction],
        inputs: ControllerInputs,
        menu: bool
):
    active_move_actions = [
        action
        for key, action in move_actions.items()
        if key in (inputs.up if menu else inputs.pressed)
    ]
    active_tool_actions = [
        action
        for key, action in tool_actions.items()
        if key in inputs.up
    ]
    result_action = functools.reduce(
        lambda a1, a2: a1 | a2,
        active_move_actions,
        PlayerAction.NONE
    )
    res = functools.reduce(
        lambda a1, a2: a1 | a2,
        active_tool_actions,
        result_action
    )
    return res
