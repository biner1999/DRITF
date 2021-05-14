# Imports
# General libraries
import sys
import time
import random
import math
import numpy as np
from scipy import interpolate

# Game related libraries
import pygame
from pygame.locals import *
from pygame.joystick import *
import esper

# My files
# ECS
from components import components as com
from systems import processes as pro
from systems import carphysics as carphys
from systems import graphics
from systems import gui
from systems import particles
# Other
from other import constants
from engine import myworld

class DeltaTimeProcessor(esper.Processor):

    def process(self):
        for ent, (dt) in self.world.get_component(com.DeltaTime):
            while dt.first_time:
                dt.last_time = time.time()
                dt.first_time = False
            dt.dt = time.time() - dt.last_time
            dt.last_time = time.time()

class CollisionsProcessor(esper.Processor):
    def __init__(self, renderer, car, spoints):
        super().__init__()
        self.renderer = renderer
        self.car = car
        self.spoints = spoints

    def process(self):
        for ent, (rect) in self.world.get_component(com.Rect):
            for ent, (tmcol) in self.world.get_component(com.TileMapCollisions):
                hit_list = []
                #pygame.draw.rect(self.renderer, (255, 0, 0), rect.rect)
                for tile in tmcol.rects["layer1"]:
                    #pygame.draw.rect(self.renderer, (0, 255, 0), tile)
                    if rect.rect.colliderect(tile):
                        hit_list.append(tile)
        hit_list = []
        car_rect = self.world.component_for_entity(self.car, com.Rect).rect
        pnt = self.world.component_for_entity(self.spoints, com.SinglePoints)
        for ent, (rect) in self.world.get_component(com.Rect):
            if ent != 1:
                if car_rect.colliderect(rect.rect):
                    pnt.multiplier += 1
                    self.world.delete_entity(ent)

class DriftProcessor(esper.Processor):
    def __init__(self, renderer, car):
        super().__init__()
        self.renderer = renderer
        self.car = car

    def process(self):
        car_sar = self.world.component_for_entity(self.car, com.Steering).sar
        vel = self.world.component_for_entity(self.car, com.Velocity).velV.magnitude()

        for ent, (pnt) in self.world.get_component(com.SinglePoints):
            # When the car drifts
            if abs(car_sar) > 0.5:
                pnt.points += int((abs(car_sar) - 0.4) * vel * 5)
            # When the drift stops
            else:
                if pnt.points != 0:
                    for ent, (tpnt) in self.world.get_component(com.TotalPoints):
                        tpnt.points += pnt.points * pnt.multiplier
                    pnt.points = 0
                    pnt.multiplier = 1
                

class XXXProcessor(esper.Processor):

    def process(self):
        for ent, () in self.world.get_components():
            pass
