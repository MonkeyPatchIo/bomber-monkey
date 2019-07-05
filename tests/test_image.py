from bomber_monkey.features.display.image import Image
from bomber_monkey.utils.vector import Vector


def image_0_64_64():
    return Image('image0', Vector.create(64, 64))


def image_0_128_128():
    return Image('image0', Vector.create(128, 128))


def image_1_64_64():
    return Image('image1', Vector.create(64, 64))


def test_hashtable():
    images = {}

    image01 = image_0_64_64()
    image01b = image_0_64_64()

    image02 = image_0_128_128()
    image02b = image_0_128_128()

    image03 = image_1_64_64()
    image03b = image_1_64_64()

    assert image01 not in images
    assert image01b not in images
    assert image02 not in images
    assert image02b not in images
    assert image03 not in images
    assert image03b not in images

    images[image01] = 'image01'
    assert images[image01] == 'image01'
    assert images[image01b] == 'image01'
    assert image02 not in images
    assert image02b not in images
    assert image03 not in images
    assert image03b not in images

    images[image02] = 'image02'
    assert images[image01] == 'image01'
    assert images[image01b] == 'image01'
    assert images[image02] == 'image02'
    assert images[image02b] == 'image02'
    assert image03 not in images
    assert image03b not in images

    images[image03] = 'image03'
    assert images[image01] == 'image01'
    assert images[image01b] == 'image01'
    assert images[image02] == 'image02'
    assert images[image02b] == 'image02'
    assert images[image03] == 'image03'
    assert images[image03b] == 'image03'
