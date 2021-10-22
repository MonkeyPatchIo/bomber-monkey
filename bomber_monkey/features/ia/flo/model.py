from typing import List

import numpy as np

from bomber_monkey.features.ia.flo.layer import Layer
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


def build_model(layers: List[Layer]):
    W = {
        'run_away': {
            Layer.Empty: -1,
            Layer.Block: 1,
            Layer.Wall: 1,
            Layer.Bomb: 5,
            Layer.Explosion: 5,
            Layer.Banana: 0,
            Layer.Enemy: 0,
        },
        'pick_item': {
            Layer.Empty: 0,
            Layer.Block: 0,
            Layer.Wall: 0,
            Layer.Bomb: 0,
            Layer.Explosion: 0,
            Layer.Banana: 1,
            Layer.Enemy: 0,
        },
        'bomb_it': {
            Layer.Empty: 0,
            Layer.Block: 2,
            Layer.Wall: 0,
            Layer.Bomb: 0,
            Layer.Explosion: 0,
            Layer.Banana: -1,
            Layer.Enemy: 10,
        }
    }

    def get_weights(feature: str):
        return [W[feature][_] for _ in layers]

    features = {
        'path_finder': lambda data: data[0],
        'run_away': feature_extractor(get_weights('run_away'), loop=0),
        'pick_item': feature_extractor(get_weights('pick_item'), loop=0),
        'bomb_it': feature_extractor(get_weights('bomb_it'), loop=5),
    }

    def model(data: np.ndarray):
        return Features(**{
            name: feature(data)
            for name, feature in features.items()
        })

    return model
