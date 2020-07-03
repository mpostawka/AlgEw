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




# class Simulation(Framework):
class Simulation():
    max_score = 0
    iter_number = 0
    def __init__(self):
        # super().__init__()
        # world = self.world
        self.world = world = b2World()
        old_height = 0
        for i in range(0, 200, 10):
            height = random() * 5
            element = b2EdgeShape(
                vertices=[(-10 + i, old_height), (i, height)])
            world.CreateStaticBody(shapes=element)
            old_height = height
        body = world.CreateDynamicBody(position=(0, 4))
        body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3)
        self.body = body
        car, wheels, springs = create_vehicle(world, *random_car())

        self.car = car
        self.wheels = wheels
        self.springs = springs

    def Step(self, settings):
        # super().Step(settings)
        self.world.Step(1.0/60.0, 8, 3)
        score = self.car.position.x
        if score > self.max_score:
            self.max_score = score
        self.iter_number += 1


def test():
    s = Simulation()
    for time in range(60*100):
        s.Step(None)
    max_score, car = s.max_score, s.car
    # del s
    return (max_score, car)

if __name__ == "__main__":
    # main(Simulation)
    max_score = 0
    # for iters in tqdm(range(1000)):
    # futures = []
    # start = time.time()
    # with ThreadPoolExecutor(max_workers=20) as executor:
    #     for i in range(1000):
    #         futures.append(executor.submit(test))
    # print("Elapsed: ", time.time() - start)
    # for future in futures:
    #     try:
    #         data = future.result()
    #     except Exception as exc:
    #         print('Generated an exception: %s' % exc)
    #     if data[0] > max_score:
    #             max_score = data[0]
    #             best_car = data[1]

    # start = time.time()
    # with Pool(processes=4) as pool:
    #     # pool.map(test, range(1000))
    #     future_results = [pool.apply_async(test) for i in range(1)]
    #     results = [f.get() for f in future_results]
    #     for (score, car) in results:
    #         if score > max_score:
    #             max_score = score
    #             best_car = car
    # print("Elapsed: ", time.time() - start)

    start = time.time()
    with Pool(processes=4) as pool:
        # pool.map(test, range(1000))
        results = [test() for i in range(1000)]
        for (score, car) in results:
            if score > max_score:
                max_score = score
                best_car = car
    print("Elapsed: ", time.time() - start)

    
    print("RESULT:", max_score)
    # print("CAR:", best_car)
