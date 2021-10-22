from typing import List

import numpy as np

from bomber_monkey.features.ia.flo.features.board_layer import BoardLayer
from bomber_monkey.features.ia.flo.features.feature import Feature
from bomber_monkey.features.ia.flo.features.feature_maps import FeatureMaps
from bomber_monkey.features.ia.flo.utils import feature_extractor


def build_model(layers: List[BoardLayer]):
    W = {
        Feature.PathFinder: {
            BoardLayer.Empty: 1,
            BoardLayer.Block: 0,
            BoardLayer.Wall: -1,
            BoardLayer.Bomb: 0,
            BoardLayer.Explosion: 0,
            BoardLayer.Banana: 0,
            BoardLayer.Enemy: 0,
        },
        Feature.Threat: {
            BoardLayer.Empty: 0,
            BoardLayer.Block: 1,
            BoardLayer.Wall: 1,
            BoardLayer.Bomb: 10,
            BoardLayer.Explosion: 1,
            BoardLayer.Banana: 0,
            BoardLayer.Enemy: 0,
        },
        Feature.PickupTarget: {
            BoardLayer.Empty: 0,
            BoardLayer.Block: 0,
            BoardLayer.Wall: 0,
            BoardLayer.Bomb: 0,
            BoardLayer.Explosion: 0,
            BoardLayer.Banana: 1,
            BoardLayer.Enemy: 0,
        },
        Feature.BombTarget: {
            BoardLayer.Empty: 0,
            BoardLayer.Block: 1,
            BoardLayer.Wall: 0,
            BoardLayer.Bomb: -10,
            BoardLayer.Explosion: 0,
            BoardLayer.Banana: 0,
            BoardLayer.Enemy: 10,
        }
    }

    def get_weights(feature: Feature):
        return [W[feature][_] for _ in layers]

    SMOOTH = 1

    features = {
        feat: feature_extractor(get_weights(feat), loop=loop)
        for feat, loop in [
            (Feature.PathFinder, 0),
            (Feature.BombTarget, SMOOTH),
            (Feature.PickupTarget, SMOOTH),
            (Feature.Threat, SMOOTH),
        ]
    }

    def model(data: np.ndarray):
        h, w = data.shape[1:]
        maps = FeatureMaps(list(features.keys()), w, h)
        for feat, feature in features.items():
            maps.add(feat, feature(data))
        return maps

    return model
