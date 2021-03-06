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
import myworld

# Intializations of PyGame modules
pygame.init()
pygame.font.init()
pygame.joystick.Joystick(0).init()

# Fonts
myfont = pygame.font.SysFont('Comic Sans MS', 100)
mysmallfont = pygame.font.SysFont('Comic Sans MS', 50)

# Joystick
joysticks = [pygame.joystick.Joystick(x) 
for x in range(pygame.joystick.get_count())]

# Set up a window and a window resolution
pygame.display.set_caption("DRITF!")
win_res = (1920, 1080)
screen = pygame.display.set_mode(win_res,0,32)

"""

# Create a game world
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

world.add_component(car, com.Sprite(sprite=img))

world.add_component(car, com.Position(initV=([960/28, 540/28])))
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
world.add_component(car, com.Rect(960, 540, img.get_width(), img.get_height()))

tiled_map = pytmx.load_pygame("assets/maps/untitled.tmx")

tilemap = world.create_entity(com.TileMap(tilemap=tiled_map), com.Camera(posV=[0,0],offset_x=screen.get_width()/2, offset_y=screen.get_height()/2), com.TileMapCollisions())

tyre_smoke_right = world.create_entity(com.Particles(angle_offset=0.4))
tyre_smoke_left = world.create_entity(com.Particles(angle_offset=-0.4))



tpoints = world.create_entity(com.Text("0", "Arial", 40, 1), com.Surface(400, 80, (0, 0, 0, 80)), com.Location(0, 0), com.TotalPoints())
spoints = world.create_entity(com.Text("0", "Arial", 40, 1), com.Surface(400, 80, (0, 0, 0, 80)), com.Location(450, 0), com.SinglePoints())

speed = world.create_entity(com.Text("0", "Arial", 70, 2), com.Surface(140, 80, (255, 140, 0, 80)), com.Location(1550, 950))
gear = world.create_entity(com.Text("N", "Arial", 70, 2), com.Surface(100, 80, (255, 140, 0, 80)), com.Location(1700, 950))
timer = world.create_entity(com.Text("0", "Arial", 70, 2), com.Surface(200, 80, (0, 0, 0, 80)), com.Location(1920-200,0), com.Time(time=15), com.DeltaTime())



cone = pygame.image.load("assets/cone_straight.png")

marker = world.create_entity(com.Sprite(cone), com.Location(620, 2200), com.Angle(0), com.ObjectCollisions(), com.Rect(620, 2200, cone.get_width(), cone.get_height()))
# Processors
#world.add_processor(carphys.TestProcessor())
world.add_processor(carphys.SteeringProcessor())
world.add_processor(carphys.RPMTorqueProcessor())
world.add_processor(carphys.FForceProcessor())
world.add_processor(carphys.AccelerationProcessor())
world.add_processor(carphys.VelocityProcessor())
world.add_processor(carphys.PositionProcessor())

world.add_processor(graphics.RenderProcessor(renderer=screen), priority=2)

world.add_processor(graphics.TileMapProcessor(renderer=screen), priority=3)
world.add_processor(graphics.CameraProcessor(renderer=screen), priority=4)

world.add_processor(particles.AddParticlesProcessor(), priority=2)
world.add_processor(particles.RenderParticlesProcessor(renderer=screen), priority=3)
world.add_processor(pro.CollisionsProcessor(renderer=screen))

world.add_processor(gui.Gear())
world.add_processor(gui.Speed())
world.add_processor(gui.TotalPointsCalculaton())
world.add_processor(gui.SinglePointsCalculaton())

world.add_processor(gui.Timer())
world.add_processor(gui.Speedometer(renderer=screen))
world.add_processor(gui.DisplayBoxText(renderer=screen))

world.add_processor(graphics.RenderObjectsProcessor(renderer=screen), priority=2)

world.add_processor(pro.DriftProcessor(renderer=screen))

"""

def drawTextCentred(font, text, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    surface.blit(textobj, (x - textrect.width/2, y - textrect.height/2))

def drawTextLeft(font, text, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    surface.blit(textobj, (x, y - textrect.height/2))

def slider(surface,
            bar_width, bar_height, bar_xpos, bar_ypos, bar_color,
            thing_width, thing_color, current_value,
            min_val, max_val,
            mx, my, click):

    actual_bar_width = bar_width - thing_width
    range_val = max_val - min_val
    interval = actual_bar_width/range_val

    thing_pos = (current_value-min_val)*interval+bar_xpos

    if mx < bar_xpos:
        mx = bar_xpos
    elif mx > bar_xpos - thing_width + bar_width:
        mx = bar_xpos - thing_width + bar_width
    
    slider_bar = pygame.Rect(bar_xpos, bar_ypos, bar_width, bar_height)
    pygame.draw.rect(screen, bar_color, slider_bar)
    if slider_bar.collidepoint((mx, my)):
        if click:
            thing_pos = mx
        
    slider_thing = pygame.Rect(thing_pos, bar_ypos, thing_width, bar_height)
    pygame.draw.rect(screen, thing_color, slider_thing)
    actual_thing_pos = thing_pos - bar_xpos
    val = min_val + round(actual_thing_pos/interval)
    world.component_for_entity(car, com.Steering).max_angle = val

def modifyLoop():
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
            click = pygame.mouse.get_pressed()[0]

        screen.fill((100,5,5))

        mx, my = pygame.mouse.get_pos()
        slider(screen, screen.get_width()/4*2, 50, screen.get_width()/4, 400, (155, 155, 155), 30, (255, 255, 255), world.component_for_entity(car, com.Steering).max_angle, 30, 80, mx, my, click)
        drawTextCentred(mysmallfont, str(world.component_for_entity(car, com.Steering).max_angle), (0, 0, 0), screen, screen.get_width()/6*5, 400+25)
        drawTextCentred(mysmallfont, "Steering Angle", (0, 0, 0), screen, screen.get_width()/2, 400-25)

        back_button = pygame.Rect(50, 50, 300, 120)
        pygame.draw.rect(screen, (240, 240, 240), back_button) 

        drawTextCentred(myfont, "DRITF!", (155, 155, 155), screen, screen.get_width()/2, screen.get_height()/5)

        drawTextCentred(myfont, "BACK", (0, 0, 0), screen, (back_button.x + back_button.width/2), (back_button.y + back_button.height/2))

        if back_button.collidepoint((mx, my)):
            if click:
                running = False
        
        dt = time.time() - last_time
        last_time = time.time()

        pygame.display.update()
        clock.tick(constants.TARGET_FRAMERATE)

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
                modifyLoop()
        click = False
        
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
        world.component_for_entity(timer, com.DeltaTime).dt = dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT:
                    pass
            if event.type == pygame.JOYBUTTONDOWN:
                #Go back to main menu
                if pygame.joystick.Joystick(0).get_button(7):
                    running = False
                #Gear down
                if pygame.joystick.Joystick(0).get_button(4):
                    if world.component_for_entity(car, com.GearBox).current_gear > 0:
                        world.component_for_entity(car, com.GearBox).current_gear -= 1
                        #print(world.component_for_entity(car, com.GearBox).current_gear)

                #Gear up
                if pygame.joystick.Joystick(0).get_button(5):
                    if world.component_for_entity(car, com.GearBox).current_gear < world.component_for_entity(car, com.GearBox).no_of_gears-1:
                        world.component_for_entity(car, com.GearBox).current_gear += 1
                        #print(world.component_for_entity(car, com.GearBox).current_gear)
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
                    world.component_for_entity(car, com.Steering).steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 + 0.25)*-world.component_for_entity(car, com.Steering).max_angle)
                elif pygame.joystick.Joystick(0).get_axis(0) > 0.2:
                    world.component_for_entity(car, com.Steering).steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 - 0.25)*-world.component_for_entity(car, com.Steering).max_angle)
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
        #speedo()
        #pygame.draw.rect(screen, (255, 0, 0), (world.component_for_entity(car, com.Position).posV.x, world.component_for_entity(car, com.Position).posV.y, world.component_for_entity(car, com.Sprite).sprite.get_width(), world.component_for_entity(car, com.Sprite).sprite.get_height()))

        # Updates display
        pygame.display.update()
        clock.tick(constants.TARGET_FRAMERATE)


menuLoop()

# Quit
#pygame.joystick.quit()
pygame.quit()


## How I about wanted to go about implementation initially and compare to what it is
## Modify the list of features to fit the project
## 