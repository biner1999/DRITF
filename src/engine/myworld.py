# Imports
# General libraries
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
from systems import processes as pro
from systems import carphysics as carphys
from systems import graphics
from systems import gui
from systems import particles
from engine import states as sta
# Other
from other import constants

class MyWorld():
    def __init__(self, screen):
        self.world, self.entities = self.build_world(screen)

        self.states = self.world.create_entity(com.States())
        self.world.add_processor(sta.StateProcessor(screen, self.entities))

    def build_world(self, screen):
        world = esper.World()

        car = self.create_car_entity(world)
        tilemap = self.create_tilemap_entity(world, screen)
        tyre_smoke_left, tyre_smoke_right = self.create_smoke_entity(world)
        marker = self.create_marker_entities(world)
        tpoints, spoints, speed, gear, timer = self.create_hud_entities(world)
        background = self.create_background_entity(world)
        play_button = self.create_play_button_entity(world, screen)
        tuning_button = self.create_tuning_button_entity(world, screen)
        back_to_menu_button = self.create_back_to_menu_button_entity(world, screen)
        steering_angle_slider = self.create_steering_angle_slider_entity(world, screen, car)
        rear_diff_slider = self.create_rear_diff_slider_entity(world, screen, car)
        mass_slider = self.create_mass_slider_entity(world, screen, car)
        cg_slider = self.create_cg_slider_entity(world, screen, car)
        
        entities = {"car":car, "tilemap":tilemap, "tyre_smoke_left":tyre_smoke_left, "tyre_smoke_right":tyre_smoke_right, "marker":marker, "tpoints":tpoints, "spoints":spoints, "speed":speed, "gear":gear, "timer":timer}

        return world, entities

    def create_steering_angle_slider_entity(self, world, screen, car):
        steering_angle_slider = world.create_entity(com.Text("Steering Angle (degrees)", "Arial", 40, 2), com.Slider(bar_width=screen.get_width()/4*2, bar_height=50, bar_x=screen.get_width()/4, bar_y=200, bar_color=(155,155,155), slider_width=30, slider_color=(255,255,255), current_val=world.component_for_entity(car, com.Steering).max_angle, min_val=30, max_val=80, rounding=0))

        return steering_angle_slider

    def create_rear_diff_slider_entity(self, world, screen, car):
        rear_diff_slider = world.create_entity(com.Text("Rear differential ratio", "Arial", 40, 2), com.Slider(bar_width=screen.get_width()/4*2, bar_height=50, bar_x=screen.get_width()/4, bar_y=350, bar_color=(155,155,155), slider_width=30, slider_color=(255,255,255), current_val=world.component_for_entity(car, com.GearBox).rear_diff, min_val=2, max_val=5, rounding=3))

        return rear_diff_slider

    def create_mass_slider_entity(self, world, screen, car):
        mass_slider = world.create_entity(com.Text("Mass (kg)", "Arial", 40, 2), com.Slider(bar_width=screen.get_width()/4*2, bar_height=50, bar_x=screen.get_width()/4, bar_y=500, bar_color=(155,155,155), slider_width=30, slider_color=(255,255,255), current_val=world.component_for_entity(car, com.Chassis).mass, min_val=800, max_val=2000, rounding=0))

        return mass_slider
    
    def create_cg_slider_entity(self, world, screen, car):
        cg_slider = world.create_entity(com.Text("Centre of gravity (m)", "Arial", 40, 2), com.Slider(bar_width=screen.get_width()/4*2, bar_height=50, bar_x=screen.get_width()/4, bar_y=650, bar_color=(155,155,155), slider_width=30, slider_color=(255,255,255), current_val=world.component_for_entity(car, com.Chassis).cg_height, min_val=0.30, max_val=0.60, rounding=2))
        
        return cg_slider

    def create_play_button_entity(self, world, screen):
        play_button = world.create_entity(com.Rect(screen.get_width()/2-150, screen.get_height()/3, 300, 120), com.Text("PLAY", "Arial", 100, 2), com.Color((240, 240, 240)), com.Button(state="menu", goto_state="game"))

        return play_button
    
    def create_tuning_button_entity(self, world, screen):
        tuning_button = world.create_entity(com.Rect(screen.get_width()/2-150, screen.get_height()/2, 300, 120), com.Text("TUNE", "Arial", 100, 2), com.Color((240, 240, 240)), com.Button(state="menu", goto_state="tuning"))

        return tuning_button

    def create_back_to_menu_button_entity(self, world, screen):
        back_to_menu_button = world.create_entity(com.Rect(5, 50, 300, 120), com.Text("BACK", "Arial", 100, 2), com.Color((240, 240, 240)), com.Button(state="tuning", goto_state="menu"))

        return back_to_menu_button

    def create_background_entity(self, world):
        background = world.create_entity(com.Background((100, 5, 5)))

        return background

    def create_car_entity(self, world):
        car = world.create_entity()
        world.add_component(car, com.DeltaTime())

        img = pygame.image.load("assets/car_black_5.png")

        torque_curve = self.torque_calc()

        world.add_component(car, com.Sprite(sprite=img))

        world.add_component(car, com.Position(initV=([430/constants.SCALE, 1190/constants.SCALE])))
        world.add_component(car, com.Velocity())
        world.add_component(car, com.Acceleration())
        world.add_component(car, com.CarAcceleration())
        world.add_component(car, com.CarVelocity())
        world.add_component(car, com.Direction(initV=([0,1]), angle=0))

        world.add_component(car, com.Chassis(wheelbase=2.57, cg_front_axle=1.208, cg_rear_axle=1.362, cg_height=0.46, mass=1222, length=4.24, width=1.775, wheel_diameter=0.5285, wheel_width=0.15, brake_power=12000, ebrake_power=5000))
        world.add_component(car, com.Engine(torque_curve=torque_curve, idle=700, rev_limit=7499, rpm=700))
        world.add_component(car, com.GearBox(4.100, -3.437, 3.626, 2.188, 1.541, 1.213, 1.000, 0.767))
        world.add_component(car, com.ForwardForce())
        world.add_component(car, com.Steering(35))
        world.add_component(car, com.ObjectCollisions())
        world.add_component(car, com.Rect(430, 1190, img.get_width(), img.get_height()))

        return car

    def create_tilemap_entity(self, world, screen):
        tiled_map = pytmx.load_pygame("assets/maps/untitled.tmx")

        tilemap = world.create_entity(com.TileMap(tilemap=tiled_map), com.Camera(posV=[0,0],offset_x=screen.get_width()/2, offset_y=screen.get_height()/2), com.TileMapCollisions())

        return tilemap

    def create_smoke_entity(self, world):
        tyre_smoke_right = world.create_entity(com.Particles(angle_offset=0.4))
        tyre_smoke_left = world.create_entity(com.Particles(angle_offset=-0.4))

        return tyre_smoke_left, tyre_smoke_right

    def create_hud_entities(self, world):
        tpoints = world.create_entity(com.Text("0", "Arial", 40, 1), com.Surface(400, 80, (0, 0, 0, 80)), com.Location(0, 0), com.TotalPoints())
        spoints = world.create_entity(com.Text("0", "Arial", 40, 1), com.Surface(400, 80, (0, 0, 0, 80)), com.Location(450, 0), com.SinglePoints())

        speed = world.create_entity(com.Text("0", "Arial", 70, 2), com.Surface(140, 80, (255, 140, 0, 80)), com.Location(1550, 950))
        gear = world.create_entity(com.Text("N", "Arial", 70, 2), com.Surface(100, 80, (255, 140, 0, 80)), com.Location(1700, 950))
        timer = world.create_entity(com.Text("0", "Arial", 70, 2), com.Surface(200, 80, (0, 0, 0, 80)), com.Location(1920-200,0), com.Time(time=25), com.DeltaTime())

        return tpoints, spoints, speed, gear, timer

    def create_marker_entities(self, world):
        cone = pygame.image.load("assets/cone_straight.png")

        marker = world.create_entity(com.Sprite(cone), com.Location(620, 2200), com.Angle(0), com.ObjectCollisions(), com.Rect(620, 2200, cone.get_width(), cone.get_height()))

        return marker

    def torque_calc(self):
        rpm = [700, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500]
        torque = [94, 108 ,122, 148, 176, 179, 167, 156, 174, 180, 177, 177, 172, 163, 133]

        yinterp = interpolate.interp1d(rpm, torque, kind="cubic")
        xnew = np.arange(700, 7500, 1)
        ynew = yinterp(xnew)
        return ynew



