import json
import numpy as np
from Box2D import (b2World, b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)

from car import create_vehicle
from terrain import (gen_terrain, parse_terrain)


class Simulation():
    quantity = 1
    max_scores = np.zeros(quantity)
    iter_number = 0

    def __init__(self, terrain=None, car=None):
        self.max_scores = np.zeros(self.quantity)
        self.world = world = b2World()
        world.CreateStaticBody(shapes=terrain)
        self.cars = [create_vehicle(world, *car)]


        # if terrain == None:
        #     try:
        #         with open("save.json") as f:
        #             save = json.load(f)
        #         terrain = parse_terrain(save['terrain'])
        #         super_car = save["car"]
        #         print("Terrain and Car loaded")
        #     except (IOError, json.JSONDecodeError):
        #         terrain = gen_terrain()
        # world.CreateStaticBody(shapes=terrain)

        # # body = world.CreateDynamicBody(position=(0, 4))
        # # body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3)
        # if car != None:
        #     self.cars = [create_vehicle(world, *car)]
        # else:
        #     self.cars_spec = super_car
        #     # self.cars_spec = [random_car() for i in range(self.quantity)]
        #     self,.cars = [create_vehicle(world, *car) for car in self.cars_spec]

    def Step(self, settings):
        self.world.Step(1.0/180.0, 30, 30)
        for i, car in enumerate(self.cars):
            score = car[i].position.x
            if score > self.max_scores[i]:
                self.max_scores[i] = score
        self.iter_number += 1

def test(car, terrain):
    s = Simulation(car=car, terrain=terrain)
    for time in range(60*100):
        s.Step(None)
    return s.max_scores[0]


# def test(terrain):
#     s = Simulation(terrain)
#     for time in range(60*100):
#         s.Step(None)
#     # del s
#     return (s.max_scores, s.cars_spec)