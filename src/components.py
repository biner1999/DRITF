import pygame
from pygame.math import *

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
        self.drive_torque = 0

class Temp:
    def __init__(self, v, t):
        self.v = v
        self.throttle = t

class Engine:
    def __init__(self, torque_curve, idle, rev_limit, rpm, throttle):
        self.torque_curve = torque_curve
        self.idle = idle
        self.rev_limit = rev_limit
        self.rpm = rpm
        self.throttle = throttle

class GearBox:
    def __init__(self, rear_diff, reverse, first, second, third, fourth, fifth, sixth, clutch_rpm):
        self.rear_diff = rear_diff
        self.gear_ratios = [reverse, 0, first, second, third, fourth, fifth, sixth]
        self.current_gear = 1
        self.no_of_gears = len(self.gear_ratios)
        self.clutch = False
        self.clutch_rpm = clutch_rpm

class ForwardForce:
    def __init__(self, forward_force):
        self.forward_force = forward_force


class AngVel:
    def __init__(self, ang_vel):
        self.ang_vel = ang_vel

class Sprite:
    def __init__(self, sprite):
        self.sprite = sprite


class Steering:
    def __init__(self, angle):
        self.angle = angle

