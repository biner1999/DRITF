import pygame
import constants
from pygame.math import *
from collections import defaultdict

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
    def __init__(self, wheelbase, cg_front_axle, cg_rear_axle, cg_height, mass, length, width, wheel_diameter, wheel_width, brake_power):
        self.wheelbase = wheelbase
        self.cg_front_axle = cg_front_axle
        self.cg_rear_axle = cg_rear_axle
        self.cg_height = cg_height
        self.mass = mass
        self.inertia = self.mass
        self.length = length
        self.width = width
        self.weight_front_standstill = cg_rear_axle/wheelbase*mass*constants.GRAVITY
        self.weight_rear_standstill = cg_front_axle/wheelbase*mass*constants.GRAVITY
        self.weight_front_dynamic = self.weight_front_standstill
        self.weight_rear_dynamic = self.weight_rear_standstill

        self.drive_torque = 0
        self.brake = 0
        self.ebrake = 0
        self.brake_power = brake_power
        self.wheel_diameter = wheel_diameter
        self.wheel_radius = self.wheel_diameter/2
        self.wheel_width = wheel_width

class Engine:
    def __init__(self, torque_curve, idle, rev_limit, rpm):
        self.torque_curve = torque_curve
        self.torque = 0
        self.idle = idle
        self.rev_limit = rev_limit
        self.rpm = rpm
        self.throttle = 0

class GearBox:
    def __init__(self, rear_diff, reverse, first, second, third, fourth, fifth, sixth):
        self.rear_diff = rear_diff
        self.gear_ratios = [reverse, 0, first, second, third, fourth, fifth, sixth]
        self.current_gear = 1
        self.no_of_gears = len(self.gear_ratios)
        self.clutch = False
        self.clutch_rpm = 0

class ForwardForce:
    def __init__(self):
        self.forward_force = 0
        self.sideway_force = 0

class Steering:
    def __init__(self):
        self.heading = 0
        self.steer_angle = 0
        self.sn = 0
        self.cs = 0
        self.fff = 0
        self.ffr = 0
        self.yawRate = 0

class TileMap:
    def __init__(self, tilemap, resolution):
        self.tilemap = tilemap
        self.resolution = resolution
        self.rects = []
        self.rects_dict = defaultdict(list)

class Camera:
    def __init__(self, posV, offset_x, offset_y):
        self.posV = pygame.Vector2(posV)
        self.offset_x = offset_x
        self.offset_y = offset_y

class Particles:
    def __init__(self):
        self.smoke = []
        self.smoke_c = []
        self.smoke_d = []
        self.decay = 0.5

class Color:
    def __init__(self, color):
        self.color = color

class Dispersion:
    def __init__(self, x, y):
        self.x = x
        self.y = y