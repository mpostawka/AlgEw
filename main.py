#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D.examples.bridge import create_bridge
from math import sqrt
from random import random
import numpy as np
import itertools
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import time

from Box2D import (b2World, b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)

from car import (basic_car, random_car, create_vehicle)
from terrain import gen_terrain



# class Simulation(Framework):
class Simulation():
    quantity = 1
    max_scores = np.zeros(quantity)
    iter_number = 0
    def __init__(self, terrain=None):
        # super().__init__()
        # world = self.world
        self.world = world = b2World()
        if terrain == None:
            terrain = gen_terrain()
        world.CreateStaticBody(shapes=terrain)
        
        # body = world.CreateDynamicBody(position=(0, 4))
        # body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3)
        self.cars = [create_vehicle(world, *random_car()) for i in range(self.quantity)]



    def Step(self, settings):
        # super().Step(settings)
        self.world.Step(1.0/60.0, 8, 3)
        for i, car in enumerate(self.cars):
            score = car[0].position.x
            if score > self.max_scores[i]:
                self.max_scores[i] = score
        self.iter_number += 1


def test(terrain):
    s = Simulation(terrain)
    for time in range(60*100):
        s.Step(None)
    max_scores = s.max_scores
    # del s
    return (max_scores, cars)

if __name__ == "__main__":
    # main(Simulation)
    start = time.time()
    terrain = gen_terrain()
    results = [test(terrain) for i in tqdm(range(100))]
    print("Elapsed: ", time.time() - start)
    print("Best: ", max(results))