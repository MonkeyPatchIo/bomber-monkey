import math

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape


def detect_collision(body1: RigidBody, shape1: Shape, body2: RigidBody, shape2: Shape):
    diff_pos_x = math.fabs(body2.pos.x - body1.pos.x)
    required_space_x = shape1.width / 2 + shape2.width / 2 - 1
    if diff_pos_x > required_space_x:
        return False
    diff_pos_y = math.fabs(body2.pos.y - body1.pos.y)
    required_space_y = shape1.height / 2 + shape2.height / 2 - 1
    if diff_pos_y > required_space_y:
        return False
    return True
