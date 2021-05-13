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
from components import components as com
import processes as pro
import carphysics as carphys
import graphics
import gui
import particles
# Other
import functions as func
import constants
import myworld

class InputProcessor(esper.Processor):

    def process(self):
        for ent, (grb, cha, ster, eng) in self.world.get_components(com.GearBox, com.Chassis, com.Steering, com.Engine):
            #print("hi")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_RIGHT:
                        pass
                if event.type == pygame.JOYBUTTONDOWN:
                    #Go back to main menu
                    if pygame.joystick.Joystick(0).get_button(7):
                        pass
                        #running = False
                    #Gear down
                    if pygame.joystick.Joystick(0).get_button(4):
                        if grb.current_gear > 0:
                            grb.current_gear -= 1
                            #print(world.component_for_entity(car, com.GearBox).current_gear)

                    #Gear up
                    if pygame.joystick.Joystick(0).get_button(5):
                        if grb.current_gear < grb.no_of_gears-1:
                            grb.current_gear += 1
                            #print(world.component_for_entity(car, com.GearBox).current_gear)
                    #Clutch
                    if pygame.joystick.Joystick(0).get_button(0):
                        grb.clutch = True
                    #Handbreak
                    if pygame.joystick.Joystick(0).get_button(1):
                        cha.ebrake = 1
                if event.type == pygame.JOYBUTTONUP:
                    #Clutch
                    if not pygame.joystick.Joystick(0).get_button(0):
                        grb.clutch = False
                    #Handbreak
                    if not pygame.joystick.Joystick(0).get_button(1):
                        cha.ebrake = 0
                if event.type == pygame.JOYAXISMOTION:
                    #UP and LEFT is negative
                    #Steering
                    if pygame.joystick.Joystick(0).get_axis(0) < -0.2:
                        ster.steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 + 0.25)*-ster.max_angle)
                    elif pygame.joystick.Joystick(0).get_axis(0) > 0.2:
                        ster.steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 - 0.25)*-ster.max_angle)
                    else:
                        ster.steer_angle = 0
                    #Throttle
                    #print("RT = " + str(pygame.joystick.Joystick(0).get_axis(5)))
                    if pygame.joystick.Joystick(0).get_axis(5) >= -0.99:
                        eng.throttle = (pygame.joystick.Joystick(0).get_axis(5) - constants.OLD_ZAXIS_MIN) * constants.RANGE_RATIO
                    if pygame.joystick.Joystick(0).get_axis(5) < -0.99:
                        eng.throttle = 0

                    #Goes from -1.0 to 1.0
                    #Break
                    #print("LT = " + str(pygame.joystick.Joystick(0).get_axis(2)))
                    if pygame.joystick.Joystick(0).get_axis(2) >= -0.99:
                        cha.brake = (pygame.joystick.Joystick(0).get_axis(2) - constants.OLD_ZAXIS_MIN) * constants.RANGE_RATIO
                    if pygame.joystick.Joystick(0).get_axis(2) < -0.99:
                        cha.brake = 0
