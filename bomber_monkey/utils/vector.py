from typing import Tuple

import numpy as np


def sign(x):
    return (-1, 1)[x > 0]


class Vector(object):

    @staticmethod
    def create(x: float = 0, y: float = 0):
        return Vector(np.array([x, y]))

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, x: float):
        self.data[0] = x

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, y: float):
        self.data[1] = y

    def as_ints(self) -> Tuple[int, int]:
        return (int(self.data[0]), int(self.data[1]))

    def __init__(self, data: np.ndarray):
        super().__init__()
        self.data = data

    def __add__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return Vector(self.data + other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return Vector(self.data - other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return Vector(self.data * other)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return Vector(self.data / other)

    def __floordiv__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return Vector(self.data // other)

    def __mod__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return Vector(self.data % other)

    def __pow__(self, power, modulo=None):
        return Vector(self.data ** power)

    def __neg__(self):
        return Vector(-self.data)

    def __repr__(self):
        return str(self.data)

    def __eq__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return np.array_equal(self.data, other)

    def __hash__(self):
        return hash((self.x, self.y))