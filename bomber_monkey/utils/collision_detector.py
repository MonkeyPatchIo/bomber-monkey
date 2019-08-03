import numpy as np

from bomber_monkey.features.physics.rigid_body import RigidBody


def detect_collision(body1: RigidBody, body2: RigidBody, ):
    dist = np.abs(body1.pos.data - body2.pos.data)
    collision_dist = body1.shape.data // 2 + body2.shape.data // 2 - 1

    return np.all(dist < collision_dist.data)
