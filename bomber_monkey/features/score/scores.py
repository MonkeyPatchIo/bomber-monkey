from typing import List

from python_ecs.ecs import Component


class Scores(Component):
    def __init__(self, scores: List[int]) -> None:
        super().__init__()
        self.scores = scores
