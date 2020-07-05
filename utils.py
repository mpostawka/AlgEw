import itertools
import json

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def save_car(car):
    with open("saved_car.json", "w") as f:
        json.dump(car, f)
        
def save_terrain(terrain_spec):
    with open("saved_terrain.json", "w") as f:
        json.dump(terrain_spec, f)