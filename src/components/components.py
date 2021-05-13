import pygame
from other import constants
from pygame.math import *
from collections import defaultdict

class DeltaTime:
    def __init__(self):
        self.dt = 0
        self.last_time = 0
        self.first_time = True

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

class Angle:
    def __init__(self, angle):
        self.angle = angle

class Chassis:
    def __init__(self, wheelbase, cg_front_axle, cg_rear_axle, cg_height, mass, length, width, wheel_diameter, wheel_width, brake_power, ebrake_power):
        self.wheelbase = wheelbase
        self.cg_front_axle = cg_front_axle
        self.cg_rear_axle = cg_rear_axle
        self.cg_height = [cg_height]
        self.mass = [mass]
        self.inertia = mass
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
        self.ebrake_power = ebrake_power
        self.wheel_diameter = wheel_diameter
        self.wheel_radius = self.wheel_diameter/2
        self.wheel_width = wheel_width

        self.tire_grip = 2

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
        self.rear_diff = [rear_diff]
        self.gear_ratios = [reverse, 0, first, second, third, fourth, fifth, sixth]
        self.current_gear = 1
        self.no_of_gears = len(self.gear_ratios)
        self.clutch = False
        self.clutch_rpm = 0
        self.trans_momentum = 0
        self.eng_momentum = 0
        self.trans_inertia = 0
        self.eng_inertia = 0

class ForwardForce:
    def __init__(self):
        self.forward_force = 0
        self.sideway_force = 0

class Steering:
    def __init__(self, max_angle):
        self.max_angle = [max_angle]
        self.heading = 0
        self.steer_angle = 0
        self.sn = 0
        self.cs = 0
        self.fff = 0
        self.ffr = 0
        self.yawRate = 0
        self.sar = 0
        self.sa = 0
        self.friction_front_left = 0
        self.friction_front_right = 0
        self.friction_rear_left = 0
        self.friction_rear_right = 0

class TileMap:
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.rects = []
        self.rects_dict = defaultdict(list)

class Camera:
    def __init__(self, posV, offset_x, offset_y):
        self.posV = pygame.Vector2(posV)
        self.offset_x = offset_x
        self.offset_y = offset_y

class Particles:
    def __init__(self, angle_offset):
        self.particles = []
        self.smoke = []
        self.smoke_c = []
        self.smoke_d = []
        self.smoke_a = []
        self.decay = 0.5
        self.angle_offset = angle_offset

class Color:
    def __init__(self, color):
        self.color = color

class Dispersion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rect:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

class TileMapCollisions:
    def __init__(self):
        self.rects = defaultdict(list)

class ObjectCollisions:
    def __init__(self):
        self.rect = None

class Text:
    def __init__(self, text, font_name, font_size, alignment):
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size)
        self.alignment = alignment

class Size:
    def __init__(self, height, width):
        self.height = height
        self.width = width

class Surface:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TotalPoints:
    def __init__(self):
        self.points = 0

class SinglePoints:
    def __init__(self):
        self.points = 0
        self.multiplier = 1

class Gear:
    def __init__(self, gear):
        self.gear = gear

class Time:
    def __init__(self, time):
        self.time = time

class States:
    def __init__(self):
        self.current_state = "menu"
        self.loaded_state = None

class Background:
    def __init__(self, color):
        self.color = color

class Button:
    def __init__(self, state, goto_state):
        self.goto_state = goto_state
        self.state = state

class Slider:
    def __init__(self, bar_width, bar_height, bar_x, bar_y, bar_color, slider_width, slider_color, current_val, min_val, max_val, rounding):
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.bar_x = bar_x
        self.bar_y = bar_y
        self.bar_color = bar_color
        self.slider_width = slider_width
        self.slider_color = slider_color
        self.current_val = current_val
        self.min_val = min_val
        self.max_val = max_val
        self.actual_bar_width = bar_width - slider_width
        self.range_val = max_val - min_val
        self.interval = (self.actual_bar_width/self.range_val)
        self.slider_pos = (current_val[0]-min_val)*self.interval+bar_x
        self.rounding = rounding
