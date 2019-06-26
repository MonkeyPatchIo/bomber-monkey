from typing import Any, Callable, Dict, Tuple, Union

from python_ecs.ecs import Component


class Keymap(Component):
    """
    https://www.pygame.org/docs/ref/key.html
    """

    def __init__(self, keymap: Dict[int, Tuple[Union[None, Callable], Union[None, Callable]]]) -> None:
        super().__init__()
        self.keymap = keymap

    def __repr__(self):
        return 'Keymap(???)'
