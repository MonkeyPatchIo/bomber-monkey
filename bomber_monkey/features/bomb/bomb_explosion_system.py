from bomber_monkey.features.board.board import Tiles, Cell
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System


class BombExplosionSystem(System):

    def __init__(self, factory: GameFactory):
        super().__init__([Bomb])
        self.factory = factory

    @property
    def board(self):
        return self.factory.board

    def update(self, dt: float, bomb: Bomb, visited: set = None) -> None:
        if not visited:
            visited = set()

        entity = bomb.entity()
        lifetime: Lifetime = entity.get(Lifetime)
        body: RigidBody = entity.get(RigidBody)

        if not lifetime or not body:
            return
        if bomb in visited or not lifetime.is_ended():
            return

        visited.add(bomb)
        cell = self.board.by_pixel(body.pos)
        if cell.tile is Tiles.WALL:
            return

        self.factory.create_explosion(cell.center)

        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            for i in range(1, bomb.explosion_size + 1):
                propagate = self.explode(dt, cell, Vector.create(*direction) * i, visited)
                if not propagate:
                    break

    def explode(self, dt: float, cell: Cell, direction: Vector, visited: set):
        cell: Cell = cell.move(direction)
        if cell is None or cell.tile == Tiles.WALL:
            return False

        self.factory.create_explosion(cell.center)

        for bomb_e in cell.get(Bomb):
            lifetime: Lifetime = bomb_e.get(Lifetime)
            lifetime.expire()
            bomb_c: Bomb = bomb_e.get(Bomb)
            self.update(dt, bomb_c, visited)

        return cell.tile is Tiles.EMPTY
