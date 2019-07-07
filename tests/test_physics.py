from bomber_monkey.features.board.board import Board
from bomber_monkey.features.physics.collision_system import PlayerCollisionSystem
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator


class Context(object):
    def __init__(self):
        self.board = Board(
            grid_size=Vector.create(5, 5),
            tile_size=Vector.create(10, 10)
        )


sim = Simulator(Context())


def test_physic_system():
    sys = PhysicSystem(friction_ratio=.5)
    body = RigidBody(
        pos=Vector.create(5, 5),
        speed=Vector.create(2, 2),
        accel=Vector.create(0, 0)
    )

    sys.update(sim, 1, body)

    assert body.speed == [1, 1]
    assert body.pos == [7, 7]


def test_player_collision():
    sys = PlayerCollisionSystem()

    body = RigidBody(
        pos=Vector.create(3, 2.5),
        speed=Vector.create(1, 0),
        accel=Vector.create(0, .5),
        shape=Shape(sim.context.board.tile_size)

    )
    sys.update(sim, 1, body)

    print(body)
