#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D.examples.bridge import create_bridge
from math import sqrt
from random import random

from Box2D import (b2World, b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)

def create_car(world, offset, wheel_radius, wheel_separation, density=1.0,
               wheel_friction=0.9, scale=(2.0, 1.0), chassis_vertices=None,
               wheel_axis=(1.0, 1.0), wheel_torques=[200.0, 100.0],
               wheel_drives=[True, False], hz=4.0, zeta=0.7, **kwargs):
    """
    """
    x_offset, y_offset = offset
    scale_x, scale_y = scale
    if chassis_vertices is None:
        chassis_vertices = [
            (-1.5, -0.5),
            (1.5, -0.5),
            (1.5, 0.0),
            (0.0, 0.9),
            (-1.15, 0.9),
            (-1.5, 0.2),
        ]

    chassis_vertices = [(scale_x * x, scale_y * y)
                        for x, y in chassis_vertices]
    radius_scale = sqrt(scale_x ** 2 + scale_y ** 2)
    wheel_radius *= radius_scale

    chassis = world.CreateDynamicBody(
        position=(x_offset, y_offset),
        fixtures=b2FixtureDef(
            shape=b2PolygonShape(vertices=chassis_vertices),
            density=density,
        )
    )

    wheels, springs = [], []
    wheel_xs = [-wheel_separation * scale_x /
                2.0, wheel_separation * scale_x / 2.0]
    for x, torque, drive in zip(wheel_xs, wheel_torques, wheel_drives):
        wheel = world.CreateDynamicBody(
            position=(x_offset + x, y_offset - wheel_radius),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=wheel_radius),
                density=density,
            )
        )

        spring = world.CreateWheelJoint(
            bodyA=chassis,
            bodyB=wheel,
            anchor=wheel.position,
            axis=wheel_axis,
            motorSpeed=0.0,
            maxMotorTorque=torque,
            enableMotor=drive,
            frequencyHz=hz,
            dampingRatio=zeta
        )

        wheels.append(wheel)
        springs.append(spring)

    return chassis, wheels, springs


# class Simulation():
class Simulation(Framework):
    def __init__(self):
        super().__init__()
        # world = b2World()
        world = self.world
        old_height = 0
        for i in range(0, 200, 10):
            height = random() * 10
            element = b2EdgeShape(vertices=[(-10 + i, old_height), (i, height)])
            world.CreateStaticBody(shapes=element)
            old_height = height
        body = world.CreateDynamicBody(position=(0,4))
        body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3)
        car, wheels, springs = create_car(self.world, offset=(
            0.0, 10.0), wheel_radius=0.8, wheel_separation=6.0, scale=(1, 1))


if __name__ == "__main__":
    main(Simulation)
    # s = Simulation()