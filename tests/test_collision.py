from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.utils.collision_detector import detect_collision
from bomber_monkey.utils.vector import Vector


def test_collision():
    body1 = RigidBody(pos=Vector.create(0, 0),
                      shape=Shape(Vector.create(10, 10)))
    assert detect_collision(
        body1,
        body1
    )

    assert not detect_collision(
        body1,
        RigidBody(pos=Vector.create(0, 10),
                  shape=Shape(Vector.create(10, 10)))
    )

    assert not detect_collision(
        body1,
        RigidBody(pos=Vector.create(10, 0),
                  shape=Shape(Vector.create(10, 10)))
    )

    assert not detect_collision(
        body1,
        RigidBody(pos=Vector.create(-10, 0),
                  shape=Shape(Vector.create(10, 10)))
    )

    assert not detect_collision(
        body1,
        RigidBody(pos=Vector.create(0, -10),
                  shape=Shape(Vector.create(10, 10)))
    )

    assert detect_collision(
        body1,
        RigidBody(pos=Vector.create(5, 5),
                  shape=Shape(Vector.create(10, 10)))
    )
