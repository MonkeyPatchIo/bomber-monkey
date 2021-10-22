from typing import List

import numpy as np

from bomber_monkey.features.ia.flo.layer import Layer
from bomber_monkey.features.ia.flo.utils import feature_extractor


class Features:
    def __init__(self,
                 path_finder: np.ndarray,
                 threat: np.ndarray,
                 attractiveness: np.ndarray,
                 bomb_it: np.ndarray,
                 ):
        self.path_finder = path_finder
        self.threat = threat
        self.attractiveness = attractiveness
        self.bomb_it = bomb_it


def build_model(layers: List[Layer]):
    W = {
        'threat': {
            Layer.Empty: -1,
            Layer.Block: 0,
            Layer.Wall: 0,
            Layer.Bomb: 10,
            Layer.Explosion: 10,
            Layer.Banana: 0,
            Layer.Enemy: 0,
        },
        'attractiveness': {
            Layer.Empty: 0,
            Layer.Block: 1,
            Layer.Wall: 0,
            Layer.Bomb: -5,
            Layer.Explosion: 0,
            Layer.Banana: 5,
            Layer.Enemy: 1,
        },
        'bomb_it': {
            Layer.Empty: 0,
            Layer.Block: 1,
            Layer.Wall: 0,
            Layer.Bomb: -1,
            Layer.Explosion: 0,
            Layer.Banana: 0,
            Layer.Enemy: 10,
        }
    }

    def get_weights(feature: str):
        return [W[feature][_] for _ in layers]

    features = {
        'path_finder': lambda data: data[0],
        'threat': feature_extractor(get_weights('threat'), loop=0),
        'attractiveness': feature_extractor(get_weights('attractiveness'), loop=0),
        'bomb_it': feature_extractor(get_weights('bomb_it'), loop=0),
    }

    def model(data: np.ndarray):
        return Features(**{
            name: feature(data)
            for name, feature in features.items()
        })

    return model
