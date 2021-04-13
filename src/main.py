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
import world
import random

# Intializations of PyGame and Joystick module
pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 100)

pygame.joystick.Joystick(0).init()
joysticks = [pygame.joystick.Joystick(x) 
for x in range(pygame.joystick.get_count())]

# Set up a window and a window resolution
pygame.display.set_caption("DRITF!")
win_res = (1920, 1080)
screen = pygame.display.set_mode(win_res,0,32)

world = esper.World()

def torque_calc():
    rpm = [700, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500]
    torque = [94, 108 ,122, 148, 176, 179, 167, 156, 174, 180, 177, 177, 172, 163, 133]

    yinterp = interpolate.interp1d(rpm, torque, kind="cubic")
    xnew = np.arange(700, 7500, 1)
    ynew = yinterp(xnew)
    return ynew

torque_curve = torque_calc()


# Car components
car = world.create_entity()

world.add_component(car, com.DeltaTime())

img = pygame.image.load("assets/car_black_5.png")
img2 = pygame.image.load("assets/arrow_yellow.png")

world.add_component(car, com.Sprite(sprite=img))

world.add_component(car, com.Position(initV=([960, 540])))
world.add_component(car, com.Velocity())
world.add_component(car, com.Acceleration())
world.add_component(car, com.CarAcceleration())
world.add_component(car, com.CarVelocity())
world.add_component(car, com.Direction(initV=([0,1]), angle=0))

world.add_component(car, com.Chassis(wheelbase=2.57, cg_front_axle=1.208, cg_rear_axle=1.362, cg_height=0.46, mass=1222, length=4.24, width=1.775, wheel_diameter=0.5285, wheel_width=0.15, brake_power=12000))
world.add_component(car, com.Engine(torque_curve=torque_curve, idle=700, rev_limit=7499, rpm=2000))
world.add_component(car, com.GearBox(4.100, -3.437, 3.626, 2.188, 1.541, 1.213, 1.000, 0.767))
world.add_component(car, com.ForwardForce())
world.add_component(car, com.Steering())

# Processors
#world.add_processor(pro.TestProcessor())
world.add_processor(pro.SteeringProcessor())
world.add_processor(pro.RPMTorqueProcessor())
world.add_processor(pro.FForceProcessor())
world.add_processor(pro.AccelerationProcessor())
world.add_processor(pro.VelocityProcessor())
world.add_processor(pro.PositionProcessor())


world.add_processor(pro.RenderProcessor(renderer=screen), priority=2)

tiled_map = pytmx.load_pygame("assets/maps/untitled.tmx")

tilemap = world.create_entity(com.TileMap(tilemap=tiled_map, resolution=128), com.Camera(posV=[0,0],offset_x=screen.get_width()/2, offset_y=screen.get_height()/2))

world.add_processor(pro.TileMapProcessor(renderer=screen), priority=3)

world.add_processor(pro.CameraProcessor(), priority=4)
tyre_smoke = world.create_entity(com.Particles())
world.add_processor(pro.AddParticlesProcessor(), priority=2)
world.add_processor(pro.RenderParticlesProcessor(renderer=screen), priority=1)

def drawTextCentred(font, text, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    surface.blit(textobj, (x - textrect.width/2, y - textrect.height/2))


def menuLoop():
    # Framerate clock
    last_time = time.time()
    clock = pygame.time.Clock()

    # Run until the user asks to quit
    running = True
    click = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        screen.fill((100,5,5))

        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(screen.get_width()/2-150, screen.get_height()/3, 300, 120)
        pygame.draw.rect(screen, (240, 240, 240), play_button)
        
        modify_button = pygame.Rect(screen.get_width()/2-150, screen.get_height()/2, 300, 120)
        pygame.draw.rect(screen, (240, 240, 240), modify_button)

        drawTextCentred(myfont, "DRITF!", (155, 155, 155), screen, screen.get_width()/2, screen.get_height()/5)

        drawTextCentred(myfont, "PLAY", (0, 0, 0), screen, (play_button.x + play_button.width/2), (play_button.y + play_button.height/2))
        drawTextCentred(myfont, "MODIFY", (0, 0, 0), screen, (modify_button.x + modify_button.width/2), (modify_button.y + modify_button.height/2))

        if play_button.collidepoint((mx, my)):
            if click:
                gameLoop()
        if modify_button.collidepoint((mx, my)):
            if click:
                pass

        dt = time.time() - last_time
        last_time = time.time()

        pygame.display.update()
        clock.tick(constants.TARGET_FRAMERATE)

def gameLoop():
    # Framerate clock
    last_time = time.time()
    clock = pygame.time.Clock()

    # Run until the user asks to quit
    running = True

    while running:
        #print(world.component_for_entity(car, com.ForwardForce).forward_force)
        #print(world.component_for_entity(car, com.Velocity).velV.magnitude()*3.6)
        # Input

        dt = time.time() - last_time
        last_time = time.time()
        world.component_for_entity(car, com.DeltaTime).dt = dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    pass
            if event.type == pygame.JOYBUTTONDOWN:
                #Gear down
                if pygame.joystick.Joystick(0).get_button(4):
                    if world.component_for_entity(car, com.GearBox).current_gear > 0:
                        world.component_for_entity(car, com.GearBox).current_gear -= 1
                        print(world.component_for_entity(car, com.GearBox).current_gear)

                #Gear up
                if pygame.joystick.Joystick(0).get_button(5):
                    if world.component_for_entity(car, com.GearBox).current_gear < world.component_for_entity(car, com.GearBox).no_of_gears-1:
                        world.component_for_entity(car, com.GearBox).current_gear += 1
                        print(world.component_for_entity(car, com.GearBox).current_gear)
                #Clutch
                if pygame.joystick.Joystick(0).get_button(0):
                    world.component_for_entity(car, com.GearBox).clutch = True
                #Handbreak
                if pygame.joystick.Joystick(0).get_button(1):
                    world.component_for_entity(car, com.Chassis).ebrake = 1
            if event.type == pygame.JOYBUTTONUP:
                #Clutch
                if not pygame.joystick.Joystick(0).get_button(0):
                    world.component_for_entity(car, com.GearBox).clutch = False
                #Handbreak
                if not pygame.joystick.Joystick(0).get_button(1):
                    world.component_for_entity(car, com.Chassis).ebrake = 0
            if event.type == pygame.JOYAXISMOTION:
                #UP and LEFT is negative
                #Steering

                if pygame.joystick.Joystick(0).get_axis(0) < -0.2:
                    world.component_for_entity(car, com.Steering).steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 + 0.25)*-35)
                elif pygame.joystick.Joystick(0).get_axis(0) > 0.2:
                    world.component_for_entity(car, com.Steering).steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 - 0.25)*-35)
                else:
                    world.component_for_entity(car, com.Steering).steer_angle = 0
                #Throttle
                #print("RT = " + str(pygame.joystick.Joystick(0).get_axis(5)))
                if pygame.joystick.Joystick(0).get_axis(5) >= -0.99:
                    world.component_for_entity(car, com.Engine).throttle = (pygame.joystick.Joystick(0).get_axis(5) - constants.OLD_ZAXIS_MIN) * constants.RANGE_RATIO
                if pygame.joystick.Joystick(0).get_axis(5) < -0.99:
                    world.component_for_entity(car, com.Engine).throttle = 0

                #Goes from -1.0 to 1.0
                #Break
                #print("LT = " + str(pygame.joystick.Joystick(0).get_axis(2)))
                if pygame.joystick.Joystick(0).get_axis(2) >= -0.99:
                    world.component_for_entity(car, com.Chassis).brake = (pygame.joystick.Joystick(0).get_axis(2) - constants.OLD_ZAXIS_MIN) * constants.RANGE_RATIO
                if pygame.joystick.Joystick(0).get_axis(2) < -0.99:
                    world.component_for_entity(car, com.Chassis).brake = 0
        

        # Background color
        #screen.fill((255, 255, 255))

        # Update the game
        world.process()
        #pygame.draw.rect(screen, (255, 0, 0), (world.component_for_entity(car, com.Position).posV.x, world.component_for_entity(car, com.Position).posV.y, world.component_for_entity(car, com.Sprite).sprite.get_width(), world.component_for_entity(car, com.Sprite).sprite.get_height()))

        # Updates display
        pygame.display.update()
        clock.tick(constants.TARGET_FRAMERATE)


menuLoop()

# Quit
#pygame.joystick.quit()
pygame.quit()
