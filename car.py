from Box2D import (b2World, b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi, b2Filter)
import math
from random import random
import numpy as np

VERTICES_COUNT = 6
PARAMETERS_COUNT = 10
WHEEL_COUNT = 2
PARAMETERS = ["position_x", "position_y", "radius", "density", "wheel_axis_x", "wheel_axis_y", "speed", "torque", "enable_motor", "damping_ratio"]

def random_car(lenght = 16):
    ch_verts = [(random()*5.0 - 2.5, random()*5.0 - 2.5)
                        for i in range(lenght)]
    wheels_data = [
        {
            "position_x": random()*5.0 - 2.5,
            "position_y": 10 + random()*5.0 - 2.5,
            "radius": random()*2.5,
            "density": random()* 5.0,
            "wheel_axis_x": random(),
            "wheel_axis_y": random(),
            "speed": random() * 200.0 - 100.0,
            "torque": random() * 200.0 - 100.0,
            "enable_motor": random() > 0.5,
            "damping_ratio": random(),
        }  for i in range(2)
        # for i in range(1, int(round(random() * 6)))
    ]
    return ch_verts, wheels_data

    

def create_vehicle(world, chassis_vertices, wheels_data):
    chassis_vertices = sorted(chassis_vertices, key=lambda cord: cord[0])
    shapes = [b2PolygonShape(vertices=[chassis_vertices[i], chassis_vertices[i+1],
        chassis_vertices[i+2], chassis_vertices[i+3]]) for i in range(0, len(chassis_vertices) - 2, 2)]
    
    chassis = world.CreateDynamicBody(
        position=(0, 10),
        shapes=shapes,
        shapeFixture=b2FixtureDef(density=1, filter=b2Filter(groupIndex= -1)),
    )
    wheels, springs = [], []
    for wheel_spec in wheels_data:
        wheel = world.CreateDynamicBody(
            position=(wheel_spec["position_x"], wheel_spec["position_y"]),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=wheel_spec["radius"]),
                density=wheel_spec["density"],
                filter=b2Filter(groupIndex= -1),
            )
        )

        spring = world.CreateWheelJoint(
            bodyA=chassis,
            bodyB=wheel,
            anchor=wheel.position,
            axis=(wheel_spec["wheel_axis_x"], wheel_spec["wheel_axis_y"]),
            motorSpeed=wheel_spec["speed"],
            maxMotorTorque=wheel_spec["torque"],
            enableMotor=wheel_spec["enable_motor"],
            dampingRatio=wheel_spec["damping_ratio"],
            frequencyHz=4.0
        )

        wheels.append(wheel)
        springs.append(spring)
    return chassis, wheels, springs

def basic_car():
    ch_verts = [
        (1.0, 0.0),
        (0.5, 0.55),
        (1.0, -1.0),
        (-1.0, -1.0),children_population_solutions
        (-1.0, 0.0),
        (1.0, 0.0),
    ]

    wheels_data = [
        {
            "position_x": 1.5,
            "position_y": 8.7,
            "radius": 0.5,
            "density": 1.0,
            "wheel_axis_x": 0.0,
            "wheel_axis_y": 1.0,
            "speed": -10.0,
            "torque": 50.0,
            "enable_motor": True,
            "damping_ratio": 0.7,
        },
        {
            "position_x": -1.5,
            "position_y": 8.7,
            "radius": 0.5,
            "density": 1.0,
            "wheel_axis_x": 0.0,
            "wheel_axis_y": 1.0,
            "speed": -10.0,
            "torque": 50.0,
            "enable_motor": True,
            "damping_ratio": 0.7,
        },
    ]
    return ch_verts, wheels_data

def car_to_code(car):
    ch_verts, wheels_data = car
    return np.append(
        np.array(ch_verts).reshape(len(ch_verts) * 2),
        [[
            wheels_data[i][parameter] for parameter in PARAMETERS
        ] for i in range(WHEEL_COUNT)]
    )
    
def code_to_car(code):
    vertices = code[:VERTICES_COUNT * 2]
    ch_verts = [(vertices[i], vertices[i+1]) for i in range(0, VERTICES_COUNT * 2, 2)]
    data = code[VERTICES_COUNT * 2:]
    wheels_data = []
    for wheel_offset in range(0, len(data), PARAMETERS_COUNT):
        wheel = dict()
        for i, parameter in enumerate(PARAMETERS):
            wheel[parameter] = data[wheel_offset + i]
        # wheel["enable_motor"] = wheel["enable_motor"] > 0
        wheel["enable_motor"] = True
        wheel["position_y"] += 15
        wheel["wheel_axis_x"] = 0.0
        wheel["wheel_axis_y"] = 1.0
        wheel["speed"] = -20.0
        wheel["torque"] += 50.0

        wheels_data.append(wheel)
    return ch_verts, wheels_data

def is_car_valid(car):
    limits = {
            "position_x": (-7, 7),
            "position_y": (10, 20), 
            "radius": (0.2, 4.0),
            "density": (0.3, 5.0),
            "wheel_axis_x": (-1, 1),
            "wheel_axis_y": (-1, 1),
            "speed": (-100.0, 100.0),
            "torque": (0.0, 200.0),
            "enable_motor": (-10.0, 10.0),
            "damping_ratio": (0.3, 0.9),
    }
    ch_verts, wheels_data = car

    for i, (x1, y1) in enumerate(ch_verts):
        for j, (x2, y2) in enumerate(ch_verts):
            if i != j:
                if math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < 0.1:
                    return False
    
    for x, y in ch_verts:
        if abs(x) > 5.0 or abs(y) > 5.0:
            return False

    for wheel in wheels_data:
        for parameter, value in limits.items():
            if wheel[parameter] < value[0] or wheel[parameter] > value[1]:
                return False
    
    return True
