from typing import Callable

from bomber_monkey.features.controller.input_mapping import InputMapping


class ControllerDescriptor:
    def __init__(self, name: str, factory: Callable[[], InputMapping]):
        self.name = name
        self.factory = factory

    @property
    def input_mapping(self):
        return self.factory()
