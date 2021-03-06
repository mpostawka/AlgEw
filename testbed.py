#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Box2D.examples.framework import Framework, Keys, main
from Box2D.examples.bridge import create_bridge
from random import random
import numpy as np
import json

from Box2D import (
    b2World,
    b2CircleShape,
    b2EdgeShape,
    b2FixtureDef,
    b2PolygonShape,
    b2_pi,
)

from car import basic_car, random_car, create_vehicle
from terrain import gen_terrain, parse_terrain


class Simulation(Framework):
    quantity = 1
    max_scores = np.zeros(quantity)
    iter_number = 0
    last_x = 0

    def __init__(self, terrain=None):
        self.max_scores = np.zeros(self.quantity)
        super().__init__()
        world = self.world
        # if terrain == None:
        #     try:
                # with open("saved_terrain.json") as f:
                #     terrain = parse_terrain(json.load(f))
        with open("saved_car.json") as f:
            super_car = json.load(f)
        print("Terrain and Car loaded")
            #     print(super_car[0])
            # except (IOError, json.JSONDecodeError):
            #     terrain = gen_terrain()
        terrain, _ = gen_terrain()
        world.CreateStaticBody(shapes=terrain)

        self.cars_spec = [(super_car[0], super_car[1])]
        self.cars = [create_vehicle(world, *car) for car in self.cars_spec]

    def Step(self, settings):
        super().Step(settings)
        self.viewCenter = (self.cars[0][0].position.x, 20)
        print(self.last_x - self.cars[0][0].position.x)
        self.last_x = self.cars[0][0].position.x


if __name__ == "__main__":
    main(Simulation)
