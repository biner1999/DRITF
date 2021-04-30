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
import pytmx

# My files
# ECS
import components as com
import processes as pro
import carphysics as carphys
import graphics
import gui
import particles
# Other
import functions as func
import constants
import world

class CollisionsProcessor(esper.Processor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

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
        car_rect = self.world.component_for_entity(1, com.Rect).rect
        for ent, (rect) in self.world.get_component(com.Rect):
            if ent != 1:
                if car_rect.colliderect(rect.rect):
                    hit_list.append(rect.rect)


class DriftProcessor(esper.Processor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        car_sar = self.world.component_for_entity(1, com.Steering).sar
        vel = self.world.component_for_entity(1, com.Velocity).velV.magnitude()
        for ent, (pnt) in self.world.get_component(com.SinglePoints):
            if abs(car_sar) > 0.6:
                pnt.points += int((abs(car_sar) - 0.4) * vel*0.5 * 10)
                #print(points)
            else:
                if pnt.points != 0:
                    for ent, (tpnt) in self.world.get_component(com.TotalPoints):
                        tpnt.points += pnt.points
                    pnt.points = 0
                

class XXXProcessor(esper.Processor):

    def process(self):
        for ent, () in self.world.get_components():
            pass
