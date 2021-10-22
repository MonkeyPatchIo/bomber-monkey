from typing import Optional

from bomber_monkey.features.board.board import Tiles, TileEffect, Cell
from bomber_monkey.features.physics.collision import Collision
from bomber_monkey.features.player.stronger import Stronger
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System, Simulator, Component


class Crunching(Component):
    def __init__(self, cell: Cell) -> None:
        super().__init__()
        self.time = 0
        self.cell = cell


class CrunchSystem(System):

    def __init__(self, conf: GameConfig):
        super().__init__([Collision, Stronger])
        self.conf = conf

    def update(self, sim: Simulator, dt: float, collision: Collision, stronger: Stronger) -> None:
        cell = next(filter(lambda c: c.tile == Tiles.BLOCK, collision.cells), None)
        if cell is not None:
            entity = stronger.entity()
            crunching: Optional[Crunching] = entity.get(Crunching)
            if crunching is None:
                entity.attach(Crunching(cell))
                cell.effect = TileEffect.SHAKING
            else:
                crunching.time += dt
                if crunching.time > self.conf.crushing_wait_duration:
                    cell.tile = Tiles.EMPTY
                    cell.effect = TileEffect.NONE
                    crunching.delete()


class NoCrunchSystem(System):

    def __init__(self):
        super().__init__([Crunching])

    def update(self, sim: Simulator, dt: float, crunching: Crunching) -> None:
        entity = crunching.entity()
        collision: Optional[Collision] = entity.get(Collision)
        if collision is None or crunching.cell not in collision.cells:
            crunching.cell.effect = TileEffect.NONE
            crunching.delete()
