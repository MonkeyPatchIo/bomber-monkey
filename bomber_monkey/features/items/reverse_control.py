from bomber_monkey.features.controller.input_mapping import InputMapping
from bomber_monkey.features.items.item import consume_item
from python_ecs.ecs import Component
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System, Simulator


class ReserveControlItem(Component):
    def __init__(self) -> None:
        super().__init__()


class ReserveControlItemSystem(System):

    def __init__(self):
        super().__init__([ReserveControlItem, RigidBody])

    def update(self, sim: Simulator, dt: float, reverse_control: ReserveControlItem, body: RigidBody) -> None:
        player_entity = consume_item(sim, reverse_control, body)
        if player_entity is not None:
            input: InputMapping = player_entity.get(InputMapping)
            input.reversed = not input.reversed
