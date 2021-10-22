from pathlib import Path

import numpy as np

from bomber_monkey.features.ia.flo.layers.feature import Feature
from bomber_monkey.features.ia.flo.utils import normalize


class FeatureMaps:
    def __init__(self):
        self.maps = {}

    def add(self, feature: Feature, map: np.ndarray):
        self.maps[feature] = map

    def get(self, feature: Feature):
        return self.maps[feature]

    def debug(self, label: str, frame: int, zoom: int = 20):
        import cv2
        export = Path('/tmp/features')
        export.mkdir(parents=True, exist_ok=True)

        maps = list(self.maps.values())

        maps = map(normalize, maps)
        data = np.vstack(list(maps))
        data = np.kron(data, np.ones((zoom, zoom)))

        full_path = export / f'{frame}_{label}.png'
        cv2.imwrite(str(full_path), data * 255)
