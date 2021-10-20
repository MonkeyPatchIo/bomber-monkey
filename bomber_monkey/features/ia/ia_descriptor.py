from typing import Callable

from bomber_monkey.features.ia.ia_interface import IA


class IADescriptor:
    def __init__(self, name: str, key_description: str, key: int, ia_factory: Callable[[], IA]):
        self.name = name
        self.key_description = key_description
        self.key = key
        self.ia_factory = ia_factory


