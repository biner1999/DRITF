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
import inputt
import components as com
import processes as pro
import carphysics as carphys
import graphics
import gui
import particles
import menus

# Other
import functions as func
import constants

class LoadUnloadd:

    def load_game(self, world, screen, entities):

        world.add_processor(pro.DeltaTimeProcessor(), 900)

        #world.add_processor(inputt.InputProcessor(), 800)

        world.add_processor(carphys.SteeringProcessor())
        world.add_processor(carphys.RPMTorqueProcessor())
        world.add_processor(carphys.FForceProcessor())
        world.add_processor(carphys.AccelerationProcessor())
        world.add_processor(carphys.VelocityProcessor())
        world.add_processor(carphys.PositionProcessor())
        world.add_processor(pro.CollisionsProcessor(renderer=screen, car=entities["car"], spoints=entities["spoints"]))

        world.add_processor(graphics.TileMapProcessor(renderer=screen), priority=3)
        world.add_processor(graphics.CameraProcessor(renderer=screen, car=entities["car"]), priority=4)
        world.add_processor(graphics.RenderProcessor(renderer=screen, car=entities["car"], tilemap=entities["tilemap"]), priority=2)
        world.add_processor(graphics.RenderObjectsProcessor(renderer=screen, tilemap=entities["tilemap"]), priority=2)

        world.add_processor(particles.AddParticlesProcessor(car=entities["car"], tilemap=entities["tilemap"]), priority=2)
        world.add_processor(particles.RenderParticlesProcessor(renderer=screen), priority=3)

        world.add_processor(gui.Gear(gear=entities["gear"]))
        world.add_processor(gui.Speed(speed=entities["speed"]))
        world.add_processor(gui.TotalPointsCalculaton())
        world.add_processor(gui.SinglePointsCalculaton())

        world.add_processor(gui.Timer())
        world.add_processor(gui.Speedometer(renderer=screen, car=entities["car"]))
        world.add_processor(gui.DisplayBoxText(renderer=screen))
        world.add_processor(pro.DriftProcessor(renderer=screen, car=entities["car"]))

    def unload_game(self, world):
        world.remove_processor(pro.DeltaTimeProcessor)

        #world.remove_processor(inputt.InputProcessor)
        world.remove_processor(carphys.RPMTorqueProcessor)
        world.remove_processor(carphys.SteeringProcessor)
        world.remove_processor(carphys.FForceProcessor)
        world.remove_processor(carphys.AccelerationProcessor)
        world.remove_processor(carphys.VelocityProcessor)
        world.remove_processor(carphys.PositionProcessor)
        world.remove_processor(pro.CollisionsProcessor)

        world.remove_processor(graphics.TileMapProcessor)
        world.remove_processor(graphics.CameraProcessor)
        world.remove_processor(graphics.RenderProcessor)
        world.remove_processor(graphics.RenderObjectsProcessor)

        world.remove_processor(particles.AddParticlesProcessor)
        world.remove_processor(particles.RenderParticlesProcessor)

        world.remove_processor(gui.Gear)
        world.remove_processor(gui.TotalPointsCalculaton)
        world.remove_processor(gui.SinglePointsCalculaton)

        world.remove_processor(gui.Timer)
        world.remove_processor(gui.Speedometer)
        world.remove_processor(gui.DisplayBoxText)
        world.remove_processor(pro.DriftProcessor)

    def load_menu(self, world, renderer, entities):
        world.add_processor(menus.BackgroundProcessor(renderer))
        world.add_processor(menus.ButtonProcessor(renderer))
    """

                screen.fill((100,5,5))
                drawTextCentred(myfont, "DRITF!", (155, 155, 155), screen, screen.get_width()/2, screen.get_height()/5)

                """
        #world.add_processor(pro.)

    def unload_menu(self, world):
        world.remove_processor(menus.BackgroundProcessor)
        world.remove_processor(menus.ButtonProcessor)
        #world.remove_processor(pro.)

    def load_tuning(self, world, renderer, entities):
        world.add_processor(menus.BackgroundProcessor(renderer))
        world.add_processor(menus.ButtonProcessor(renderer))
        world.add_processor(menus.SliderProcessor(renderer))
        """
            # Run until the user asks to quit

            screen.fill((100,5,5))

            mx, my = pygame.mouse.get_pos()
            slider(screen, screen.get_width()/4*2, 50, screen.get_width()/4, 400, (155, 155, 155), 30, (255, 255, 255), world.component_for_entity(car, com.Steering).max_angle, 30, 80, mx, my, click)
            drawTextCentred(mysmallfont, str(world.component_for_entity(car, com.Steering).max_angle), (0, 0, 0), screen, screen.get_width()/6*5, 400+25)
            drawTextCentred(mysmallfont, "Steering Angle", (0, 0, 0), screen, screen.get_width()/2, 400-25)

            back_button = pygame.Rect(50, 50, 300, 120)
            pygame.draw.rect(screen, (240, 240, 240), back_button) 
            drawTextCentred(myfont, "BACK", (0, 0, 0), screen, (back_button.x + back_button.width/2), (back_button.y + back_button.height/2))

            drawTextCentred(myfont, "DRITF!", (155, 155, 155), screen, screen.get_width()/2, screen.get_height()/5)


            if back_button.collidepoint((mx, my)):
                if click:
                    running = False
            """
        #world.add_processor(pro.)

    def unload_tuning(self, world):
        world.remove_processor(menus.BackgroundProcessor)
        world.remove_processor(menus.ButtonProcessor)
        world.remove_processor(menus.SliderProcessor)
        #world.remove_processor(pro.)

class StateProcessor(esper.Processor, LoadUnloadd):

    def __init__(self, renderer, entities):
        super().__init__()
        self.renderer = renderer
        self.entities = entities

    def process(self):
        LoadUnload = LoadUnloadd()
        for ent, (state) in self.world.get_component(com.States):
            if state.current_state == "game":
                if state.loaded_state == "game":
                    pass
                else:
                    LoadUnload.unload_menu(self.world)
                    LoadUnload.unload_tuning(self.world)
                    LoadUnload.load_game(self.world, self.renderer, self.entities)
                    state.loaded_state = "game"
            elif state.current_state == "menu":
                if state.loaded_state == "menu":
                    pass
                else:
                    LoadUnload.unload_menu(self.world)
                    LoadUnload.unload_game(self.world)
                    LoadUnload.load_menu(self.world, self.renderer, self.entities)
                    state.loaded_state = "menu"
            elif state.current_state == "tuning":
                if state.loaded_state == "tuning":
                    pass
                else:
                    LoadUnload.unload_menu(self.world)
                    LoadUnload.unload_game(self.world)
                    LoadUnload.load_tuning(self.world, self.renderer, self.entities)
                    state.loaded_state = "tuning"