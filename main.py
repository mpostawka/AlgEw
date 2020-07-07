#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D.examples.bridge import create_bridge
import matplotlib.pyplot as plt
from math import sqrt
from random import random
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import time

from Box2D import (b2World, b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)

from car import (VERTICES_COUNT, PARAMETERS_COUNT, WHEEL_COUNT,
    basic_car, random_car, create_vehicle, code_to_car, car_to_code, is_car_valid)
from terrain import (gen_terrain, parse_terrain)
from utils import (save_car, save_terrain)
from genetic import es
from simulation import (test, get_objective_func)


# TODO: true value in code_to_car



def perform_evolution(objective_func):
    d = VERTICES_COUNT * 2 + PARAMETERS_COUNT * WHEEL_COUNT
    N = 1500
    T = 30
    best_objective_value, best_chromosome, history_objective_values, history_best_chromosome, history_best_sigmas = es(
        objective_func, d, N, T, 2*N, 2, 0.2, 1/np.sqrt(2*d), 1/np.sqrt(2*np.sqrt(d)), 10)
    return best_objective_value, best_chromosome, history_objective_values, history_best_chromosome, history_best_sigmas

def print_logs(args):
    best_objective_value, best_chromosome, history_objective_values, history_best_chromosome, history_best_sigmas = args
    plt.figure(figsize=(18, 4))
    plt.plot(history_objective_values[:, 0], 'r-')
    plt.plot(history_objective_values[:, 1], 'r-')
    plt.plot(history_objective_values[:, 2], 'r-')
    plt.xlabel('iteration')
    plt.ylabel('objective function value')
    plt.title('min/avg/max objective function values')
    plt.show()

    plt.figure(figsize=(18, 4))
    plt.plot(history_best_sigmas, 'r-')
    plt.xlabel('iteration')
    plt.ylabel('sigma value')
    plt.title('best sigmas'), terrain_spec
    plt.show()

if __name__ == "__main__":
    terrain, terrain_spec = gen_terrain()
    result = perform_evolution(get_objective_func(terrain))
    car = code_to_car(result[1])
    print(result)
    save_car(car)
    save_terrain(terrain_spec)
    print_logs(result)










    # start = time.time()
    # terrain, terrain_spec = gen_terrain()
    # results = [test(terrain) for i in tqdm(range(1500))]
    # scores, cars = zip(*results)
    # I = np.argmax(scores)
    # print("Best: ", scores[I])
    # print("Cars:", cars[I])
    # print("Elapsed: ", time.time() - start)
    # save_car(cars[I], terrain_spec)
