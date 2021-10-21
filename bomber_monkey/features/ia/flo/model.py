import numpy as np

from bomber_monkey.features.ia.flo.utils import feature_extractor


class Features:
    def __init__(self,
                 path_finder: np.ndarray,
                 run_away: np.ndarray,
                 pick_item: np.ndarray,
                 bomb_it: np.ndarray,
                 ):
        self.path_finder = path_finder
        self.run_away = run_away
        self.pick_item = pick_item
        self.bomb_it = bomb_it


def build_model():
    path_finder = feature_extractor(
        weights={
            'Empty': 1,
            'Block': -1,
            'Wall': 0,
            'Bomb': 0,
            'Explosion': 0,
            'Banana': 0,
            'Enemy': 0,
        }
    )

    run_away = feature_extractor(
        weights={
            'Empty': 0,
            'Block': 0,
            'Wall': 0,
            'Bomb': 1,
            'Explosion': 2,
            'Banana': 0,
            'Enemy': 0,
        }
    )

    pick_item = feature_extractor(
        weights={
            'Empty': 0,
            'Block': 0,
            'Wall': 0,
            'Bomb': 0,
            'Explosion': 0,
            'Banana': 1,
            'Enemy': 0,
        })

    bomb_it = feature_extractor(
        weights={
            'Empty': 0,
            'Block': 2,
            'Wall': 0,
            'Bomb': 0,
            'Explosion': 0,
            'Banana': -1,
            'Enemy': 10,
        })

    def model(data: np.ndarray):
        return Features(
            path_finder=path_finder(data, n=5),
            run_away=run_away(data, n=3),
            pick_item=pick_item(data, n=3),
            bomb_it=bomb_it(data, n=5),
        )

    return model
