from pathlib import Path
from typing import List

import numpy as np

from bomber_monkey.features.ia.flo.utils import normalize
from bomber_monkey.utils.timing import timing


class FeatureMaps:
    def __init__(self, features: List[str], width: int, height: int):
        self.features = features
        self.depth = len(features)
        self.mapping = {
            feature: i
            for i, feature in enumerate(features)
        }
        self.maps: np.ndarray = np.zeros((self.depth, height, width))

    def add(self, feature: str, map: np.ndarray):
        offset = self.mapping[feature]
        self.maps[offset, :, :] = map

    def get(self, feature: str):
        offset = self.mapping[feature]
        return self.maps[offset]

    def debug(self, label: str, frame: int, zoom: int = 20):
        with timing('FeatureMaps.debug'):
            import cv2
            export = Path('/tmp/features')
            export.mkdir(parents=True, exist_ok=True)

            maps = [
                self.get(feature)
                for feature in self.features
            ]

            maps = map(normalize, maps)
            data = np.vstack(list(maps))
            data = np.kron(data, np.ones((zoom, zoom)))

            full_path = export / f'{frame}_{label}.png'
            cv2.imwrite(str(full_path), data * 255)
