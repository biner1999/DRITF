# Imports
import pygame
import sys
import time
import esper
import components as com
import processes as pro
import functions as fun
import numpy as np
import math
from scipy import interpolate
import pytmx
from pygame.locals import *
from pygame.joystick import *
import constants

class World():
    def __init__(self):
        super().__init__()

        self.build_world()
    
    def build_world():
        world = esper.World()
        # All processors
        self.create_car_entity(world)

        return world

    def create_car_entity(world):
        pass
        #  All car code