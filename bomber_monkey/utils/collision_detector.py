import math
import numpy as np

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape


def detect_collision(body1: RigidBody, shape1: Shape,
                     body2: RigidBody, shape2: Shape):
    dist = np.abs(body1.pos.data - body2.pos.data)
    collision_dist = shape1.data // 2 + shape2.data // 2 - 1

    return np.all(dist < collision_dist.data)
