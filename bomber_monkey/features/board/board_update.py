from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Entity


class BoardUpdate:
    def __init__(self, added: bool, position: Vector, entity: Entity):
        self.added = added
        self.position = position
        self.entity = entity

    def __repr__(self):
        if self.added:
            return f"+ {self.entity} at {self.position}"
        return f"- {self.entity} at {self.position}"