import time

from bomber_monkey.features.board.board import Tiles, Cell, Board
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_factory import GameFactory
from python_ecs.ecs import System, Simulator


class BombExplosionSystem(System):

    def __init__(self):
        super().__init__([Bomb, Lifetime, RigidBody])

    def update(self, sim: Simulator, dt: float, bomb: Bomb, lifetime: Lifetime, body: RigidBody) -> None:
        if not lifetime.is_ended():
            return
        board: Board = sim.context.board
        cell = board.by_pixel(body.pos)
        GameFactory.create_explosion(sim, cell.center, ExplosionDirection.ALL, bomb.explosion_size)


class ExplosionPropagationSystem(System):

    def __init__(self):
        super().__init__([Explosion, RigidBody])

    def update(self, sim: Simulator, dt: float, explosion: Explosion, body: RigidBody) -> None:
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        if explosion.propagated or time.time() - explosion.start_time < conf.bomb_explosion_propagation_time:
            return
        cell = board.by_pixel(body.pos)
        if explosion.direction & ExplosionDirection.RIGHT > 0:
            self.propagate(sim, cell.right(), ExplosionDirection.RIGHT, explosion.power - 1)
        if explosion.direction & ExplosionDirection.LEFT > 0:
            self.propagate(sim, cell.left(), ExplosionDirection.LEFT, explosion.power - 1)
        if explosion.direction & ExplosionDirection.UP > 0:
            self.propagate(sim, cell.up(), ExplosionDirection.UP, explosion.power - 1)
        if explosion.direction & ExplosionDirection.DOWN > 0:
            self.propagate(sim, cell.down(), ExplosionDirection.DOWN, explosion.power - 1)
        explosion.propagated = True

    def propagate(self, sim: Simulator, cell: Cell, direction: ExplosionDirection, power: int):
        if cell is None or cell.tile == Tiles.WALL or power < 0:
            return

        for bomb_e in cell.get(Bomb):
            GameFactory.create_explosion(sim, cell.center, direction, 0)
            lifetime: Lifetime = bomb_e.get(Lifetime)
            lifetime.expire()
            direction = ExplosionDirection.ALL ^ ExplosionDirection.opposed(direction)
            bomb: Bomb = bomb_e.get(Bomb)
            GameFactory.create_explosion(sim, cell.center, direction, bomb.explosion_size)
            return

        if cell.tile == Tiles.BLOCK:
            power = 0
        GameFactory.create_explosion(sim, cell.center, direction, power)
