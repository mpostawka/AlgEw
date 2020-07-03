#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D.examples.bridge import create_bridge
from math import sqrt
from random import random
import numpy as np
import itertools

from Box2D import (b2World, b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)

from car import (basic_car, random_car, create_vehicle)




# class Simulation():
class Simulation(Framework):
    # max_score = 0
    # best_car = ()
    def __init__(self):
        super().__init__()
        world = self.world
        # world = b2World()
        # self.world = world
        old_height = 0
        for i in range(0, 200, 10):
            height = random() * 10
            element = b2EdgeShape(
                vertices=[(-10 + i, old_height), (i, height)])
            world.CreateStaticBody(shapes=element)
            old_height = height
        body = world.CreateDynamicBody(position=(0, 4))
        body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3)
        self.car = create_vehicle(world, *random_car())

    # def Step(self, settings):
    #     # super().Step(settings)
    #     self.world.Step(1.0/60.0, 8, 3)
    #     score = self.car.position.x
    #     self.viewCenter = (self.car.position.x, 20)
    #     self.Print(f"Score: {score}")
    #     if score > self.max_score:
    #         self.max_score = score


if __name__ == "__main__":
    main(Simulation)
    # for iters in range(1000):
    #     s = Simulation()
    #     for time in range(10000):
    #         s.Step(None)
    # print("RESULT:", s.max_score)
    # print("CAR:", s.best_car)
