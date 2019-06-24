from bomber_monkey.features.move.move import Position, Speed, Accel
from python_ecs.ecs import System, sim


class MoveSystem(System):
    def __init__(self):
        super().__init__([Position, Speed])

    def update(self, position: Position, speed: Speed) -> None:
        entity = sim.get(position.eid)
        accel = entity.get(Accel)
        if accel:
            speed.data += accel.data
        position.data += speed.data
