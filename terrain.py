from random import random
import numpy as np
from Box2D import b2EdgeShape


def gen_terrain():
    old_height = 0
    shapes, terrain_spec = [], []
    for i in range(0, 800, 10):
        height = random() * i / 20
        terrain_spec.append((-10 + i, old_height))
        terrain_spec.append((i, height))
        (-10 + i, old_height), (i, height)
        shapes.append(b2EdgeShape(vertices=[(-10 + i, old_height), (i, height)]))
        old_height = height
    return shapes, terrain_spec


def parse_terrain(terrain_spec):
    return [
        b2EdgeShape(vertices=[terrain_spec[i], terrain_spec[i + 1]])
        for i in range(0, len(terrain_spec), 2)
    ]
