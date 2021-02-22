import pygame
from pygame.math import *

class DeltaTime:
    def __init__(self, dt):
        self.dt = dt


class Position:
    def __init__(self, initV):
        self.posV = pygame.Vector2(initV)


class Velocity:
    def __init__(self, vel):
        self.vel = vel


class Sprite:
    def __init__(self, sprite):
        self.sprite = sprite


class Steering:
    def __init__(self, angle):
        self.angle = angle

class DirVector:
    def __init__(self, initV):
        self.dirV = pygame.math.Vector2(initV).normalize()