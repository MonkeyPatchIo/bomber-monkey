from enum import IntEnum


class AppState(IntEnum):
    MAIN_MENU = 1  # No Game launch
    IN_GAME = 2  # Game in-progress
    PAUSE_MENU = 3  # Display menu
    ROUND_END = 4  # End of round, display score
    GAME_END = 5  # End of game, display winner
