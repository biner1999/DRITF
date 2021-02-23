import pygame
from pygame.math import *

class DeltaTime:
    def __init__(self, dt):
        self.dt = dt


class Position:
    def __init__(self, initV):
        self.posV = pygame.Vector2(initV)


class Speed:
    def __init__(self, vel):
        self.speed = speed


class Sprite:
    def __init__(self, sprite):
        self.sprite = sprite


class Steering:
    def __init__(self, angle):
        self.angle = angle


class DirVector:
    def __init__(self, initV):
        self.dirV = pygame.math.Vector2(initV).normalize()


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


class Tyre:
    def __init__(self, diameter):
        self.dimaterer = diameter


class GearBox:
    def __init__(self, current_gear):
        self.current_gear = current_gear