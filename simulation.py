import json
import numpy as np
from Box2D import (
    b2World,
    b2CircleShape,
    b2EdgeShape,
    b2FixtureDef,
    b2PolygonShape,
    b2_pi,
)

from car import create_vehicle, code_to_car, is_car_valid
from terrain import gen_terrain, parse_terrain
from tqdm import tqdm


class Simulation:
    def __init__(self, terrain=None, car=None):
        self.world = world = b2World()
        world.CreateStaticBody(shapes=terrain)
        self.car, wheels, springs = create_vehicle(world, *car)

    def Step(self, settings):
        self.world.Step(1.0 / 60.0, 10, 10)


def test(car, terrain):
    max_score = 0.0
    max_score_time = 0.0
    s = Simulation(car=car, terrain=terrain)
    last_x = 0.0
    for time in range(60 * 100):
        s.Step(None)
        if s.car.position.x > max_score:
            max_score = s.car.position.x
            max_score_time = time
        if abs(s.car.position.x - last_x) > 1.0:
            max_score = 0
            break
        if time - max_score_time > 60:
            if s.car.position.x < 0:
                max_score = 0
                break
            if time - max_score_time > 600:
                break
        last_x = s.car.position.x
    return max_score


def get_objective_func(terrain):
    def objective_func(P):
        scores = []
        for code in tqdm(P):
            car = code_to_car(code)
            if is_car_valid(car):
                scores.append(test(car, terrain))
            else:
                scores.append(0.0)
        return np.array(scores)

    return objective_func
