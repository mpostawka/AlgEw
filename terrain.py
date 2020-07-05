from random import random
import numpy as np
from Box2D import b2EdgeShape

def gen_terrain():
    old_height = 0
    shapes = []
    for i in range(0, 800, 10):
        height = random() * i / 20
        shapes.append(b2EdgeShape(
            vertices=[(-10 + i, old_height), (i, height)])
        )
        old_height = height
    return shapes