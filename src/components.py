import pygame
from pygame.math import *


def bing(v):
    return v.magnitude()
class DeltaTime:
    def __init__(self, dt):
        self.dt = dt

class Acceleration:
    def __init__(self, initV):
        self.accV = pygame.Vector2(initV)

class Velocity:
    def __init__(self, initV):
        self.velV = pygame.math.Vector2(initV)

class Position:
    def __init__(self, initV):
        self.posV = pygame.Vector2(initV)


class Direction:
    def __init__(self, initV):
        self.dirV = pygame.math.Vector2(initV).normalize()


class Chassis:
    def __init__(self, wheelbase, cg_front_axle, cg_rear_axle, cg_height, mass, inertia, length, width, wheel_diameter, wheel_width):
        self.wheelbase = wheelbase
        self.cg_front_axle = cg_front_axle
        self.cg_rear_axle = cg_rear_axle
        self.cg_height = cg_height
        self.mass = mass
        self.inertia = inertia
        self.length = length
        self.width = width
        self.wheel_diameter = wheel_diameter
        self.wheel_width = wheel_width
        self.weight_front_standstill = cg_rear_axle/wheelbase*mass
        self.weight_rear_standstill = cg_front_axle/wheelbase*mass
        self.weight_front_dynamic = self.weight_front_standstill
        self.weight_rear_dynamic = self.weight_rear_standstill


class Sprite:
    def __init__(self, sprite):
        self.sprite = sprite


class Steering:
    def __init__(self, angle):
        self.angle = angle

class GearRatios:
    def __init__(self, rear_diff, reverse, first, second, third, fourth, fifth, sixth):
        self.rear_diff = rear_diff
        self.reverse = reverse
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.fifth = fifth
        self.sixth = sixth


class TopSpeed:
    def __init__(self, reverse, first, second, third, fourth, fifth, sixth):
        self.reverse = reverse
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.fifth = fifth
        self.sixth = sixth


class Wheel:
    def __init__(self, diameter):
        self.dimaterer = diameter


class GearBox:
    def __init__(self, current_gear):
        self.current_gear = current_gear