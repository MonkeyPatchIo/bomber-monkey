from python_ecs.ecs import Component


class RigidBody(Component):
    def __init__(self, mass: float = 1) -> None:
        super().__init__()
        self.mass = mass

    def __repr__(self):
        return 'RigidBody({})'.format(self.mass)
