from bomber_monkey.utils.vector import Vector


def test_equal():
    v = Vector.create(2, 4)

    assert v == [2, 4]
    assert not v == [2, 5]
    assert not v == [3, 4]


def test_add():
    v1 = Vector.create(4, 6)
    v2 = Vector.create(3, 3)

    v3 = v1 + v2
    assert v3 == [7, 9]


def test_modify():
    v = Vector.create(2, 4)

    v.x += 1
    v.y *= 5
    assert v == [3, 20]


def test_operators():
    v = Vector.create(5, 6)

    v += 2
    assert v == [7, 8]

    v = v + 3
    assert v == [10, 11]

    v = -v
    assert v == [-10, -11]

    v = v * 4
    v *= -3
    assert v == [120, 132]

    v = v % 7
    assert v == [1, 6]

    v += 4
    v = v % 7
    assert v == [5, 3]


def test_add_tuple():
    v = Vector.create(5, 6)
    v += (10, 20)
    assert v == [15, 26]


def test_mul_tuple():
    v = Vector.create(2, 3)
    v *= (5, 6)
    assert v == [10, 18]