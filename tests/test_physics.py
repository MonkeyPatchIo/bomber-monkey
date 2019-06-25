from bomber_monkey.features.board.board import Board
from bomber_monkey.features.physics.collision_system import WallCollisionSystem
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import sim

board_size = Vector.create(5, 5)
tile_size = Vector.create(10, 10)

board = sim.create(Board(
    board_size,
    tile_size
))


def test_physic_system():
    sys = PhysicSystem(friction_ratio=.5)
    body = RigidBody(
        pos=Vector.create(5, 5),
        speed=Vector.create(2, 2),
        accel=Vector.create(0, 0)
    )

    sys.update(body)

    assert body.speed == [1, 1]
    assert body.pos == [6, 6]


def test_player_collision():
    sys = WallCollisionSystem(board)

    body = RigidBody(
        pos=Vector.create(3, 2.5),
        speed=Vector.create(1, 0),
        accel=Vector.create(0, .5)
    )
    shape = Shape(tile_size)
    sys.update(body, shape)

    print(body)
