from typing import List, Optional


class GameScores:
    def __init__(self, nb_players: int):
        self.scores: List[int] = [0] * nb_players


class GameRoundResult:
    def __init__(self, scores: GameScores, winner_id: Optional[int]):
        self.scores = scores
        self.winner_id = winner_id
