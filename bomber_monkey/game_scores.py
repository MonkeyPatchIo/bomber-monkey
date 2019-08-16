from typing import List

from bomber_monkey.game_config import GameConfig


class GameScores:
    def __init__(self, conf: GameConfig):
        self.scores: List[int] = [0] * conf.PLAYER_NUMBER
