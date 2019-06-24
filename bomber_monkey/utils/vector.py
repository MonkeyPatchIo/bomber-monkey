import numpy as np


class Vector(object):

    @staticmethod
    def create(x: float, y: float):
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
        return 'Vector{}'.format(self.data)

    def __eq__(self, other):
        if isinstance(other, Vector):
            other = other.data
        return np.array_equal(self.data, other)
