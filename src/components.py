import pygame
from pygame.math import *

class DeltaTime:
    def __init__(self):
        self.dt = 0

class Sprite:
    def __init__(self, sprite):
        self.sprite = sprite

class Acceleration:
    def __init__(self):
        self.accV = pygame.Vector2([0, 0])

class Velocity:
    def __init__(self):
        self.velV = pygame.math.Vector2([0, 0])

class CarAcceleration:
    def __init__(self):
        self.accV = pygame.math.Vector2([0,0])

class CarVelocity:
    def __init__(self):
        self.velV = pygame.math.Vector2([0,0])

class Position:
    def __init__(self, initV):
        self.posV = pygame.Vector2(initV)

class Direction:
    def __init__(self, initV, angle):
        self.dirV = pygame.math.Vector2(initV).normalize()

class Chassis:
    def __init__(self, wheelbase, cg_front_axle, cg_rear_axle, cg_height, mass, inertia, length, width, wheel_diameter, wheel_width, brake, brake_power):
        self.wheelbase = wheelbase
        self.cg_front_axle = cg_front_axle
        self.cg_rear_axle = cg_rear_axle
        self.cg_height = cg_height
        self.mass = mass
        self.inertia = inertia
        self.length = length
        self.width = width
        self.wheel_diameter = wheel_diameter
        self.wheel_radius = self.wheel_diameter/2
        self.wheel_width = wheel_width
        self.weight_front_standstill = cg_rear_axle/wheelbase*mass
        self.weight_rear_standstill = cg_front_axle/wheelbase*mass
        self.weight_front_dynamic = self.weight_front_standstill
        self.weight_rear_dynamic = self.weight_rear_standstill
        self.drive_torque = 0
        self.brake = brake
        self.brake_power = brake_power

class Engine:
    def __init__(self, torque_curve, idle, rev_limit, rpm, throttle):
        self.torque_curve = torque_curve
        self.torque = 0
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
    def __init__(self):
        self.forward_force = 0
        self.sideway_force = 0

class Steering:
    def __init__(self, angle):
        self.heading = 0
        self.steer_angle = 0
        self.sn = 0
        self.cs = 0
        self.fff = 0
        self.ffr = 0
        self.yawRate = 0

