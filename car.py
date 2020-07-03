from Box2D import (b2World, b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)
from math import sqrt
from random import random

def random_car(lenght = 16):
    ch_verts = [(random()*5.0 - 2.5, random()*5.0 - 2.5)
                        for i in range(lenght)]
    wheels_data = [
        {
            "position": (random()*5.0 - 2.5, 10 + random()*5.0 - 2.5),
            "radius": 0.5,
            "density": 1.0,
            "wheel_axis": (0.0, 1.0),
            "speed": -10.0,
            "torque": 50.0,
            "enable_motor": True,
            "damping_ratio": 0.7,
        }  for i in range(int(round(random() * 6)))
    ]
    return ch_verts, wheels_data

    

def create_vehicle(world, chassis_vertices, wheels_data):
    chassis_vertices = sorted(chassis_vertices, key=lambda cord: cord[0])
    shapes = [b2PolygonShape(vertices=[chassis_vertices[i], chassis_vertices[i+1],
        chassis_vertices[i+2], chassis_vertices[i+3]]) for i in range(0, len(chassis_vertices) - 2, 2)]

    chassis = world.CreateDynamicBody(
        position=(0, 10),
        shapes=shapes,
        shapeFixture=b2FixtureDef(density=1),
    )
    wheels, springs = [], []
    for wheel_spec in wheels_data:
        wheel = world.CreateDynamicBody(
            position=wheel_spec["position"],
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=wheel_spec["radius"]),
                density=wheel_spec["density"],
            )
        )

        spring = world.CreateWheelJoint(
            bodyA=chassis,
            bodyB=wheel,
            anchor=wheel.position,
            axis=wheel_spec["wheel_axis"],
            motorSpeed=wheel_spec["speed"],
            maxMotorTorque=wheel_spec["torque"],
            enableMotor=wheel_spec["enable_motor"],
            dampingRatio=wheel_spec["damping_ratio"],
            frequencyHz=4.0
        )

        wheels.append(wheel)
        springs.append(spring)
        return chassis

def basic_car():
    ch_verts = [
        (1.0, 0.0),
        (0.5, 0.55),
        (1.0, -1.0),
        (-1.0, -1.0),
        (-1.0, 0.0),
        (1.0, 0.0),
    ]

    wheels_data = [
        {
            "position": (1.5, 8.7),
            "radius": 0.5,
            "density": 1.0,
            "wheel_axis": (0.0, 1.0),
            "speed": -10.0,
            "torque": 50.0,
            "enable_motor": True,
            "damping_ratio": 0.7,
        },
        {
            "position": (-1.5, 8.7),
            "radius": 0.5,
            "density": 1.0,
            "wheel_axis": (0.0, 1.0),
            "speed": -10.0,
            "torque": 50.0,
            "enable_motor": True,
            "damping_ratio": 0.7,
        },
    ]
    return ch_verts, wheels_data