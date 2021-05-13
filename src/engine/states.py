# Imports
# General libraries

# Game related libraries
import pygame
from pygame.locals import *
from pygame.joystick import *
import esper
import pytmx

# My files
# ECS
from components import components as com
from systems import processes as pro
from systems import carphysics as carphys
from systems import graphics
from systems import gui
from systems import particles
from systems import menus

# Other
from other import constants

class LoadUnloadd:

    def load_game(self, world, screen, entities):

        world.add_processor(pro.DeltaTimeProcessor(), 900)

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
        world.remove_processor(gui.Speed)
        world.remove_processor(gui.TotalPointsCalculaton)
        world.remove_processor(gui.SinglePointsCalculaton)

        world.remove_processor(gui.Timer)
        world.remove_processor(gui.Speedometer)
        world.remove_processor(gui.DisplayBoxText)
        world.remove_processor(pro.DriftProcessor)

    def load_menu(self, world, renderer, entities):
        world.add_processor(menus.BackgroundProcessor(renderer))
        world.add_processor(menus.ButtonProcessor(renderer))

    def unload_menu(self, world):
        world.remove_processor(menus.BackgroundProcessor)
        world.remove_processor(menus.ButtonProcessor)

    def load_tuning(self, world, renderer, entities):
        world.add_processor(menus.BackgroundProcessor(renderer))
        world.add_processor(menus.ButtonProcessor(renderer))
        world.add_processor(menus.SliderProcessor(renderer))

    def unload_tuning(self, world):
        world.remove_processor(menus.BackgroundProcessor)
        world.remove_processor(menus.ButtonProcessor)
        world.remove_processor(menus.SliderProcessor)

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
                    LoadUnload.unload_tuning(self.world)
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