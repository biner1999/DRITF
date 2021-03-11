# Imports
import pygame
import sys
import time
import esper
import components as com
import processes as pro
import functions as fun
import numpy as np
from scipy import interpolate

from pygame.locals import *
from pygame.joystick import *
import constants
# Intializations of PyGame and Joystick module
pygame.init()


pygame.joystick.Joystick(0).init()
joysticks = [pygame.joystick.Joystick(x) 
for x in range(pygame.joystick.get_count())]

# Set up a window and a window resolution
pygame.display.set_caption("DRITF!")
win_res = (1000, 1000)
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

car = world.create_entity()
world.add_component(car, com.Position(initV=([50, 50])))
world.add_component(car, com.Velocity(initV=([0, 0])))
world.add_component(car, com.Chassis(wheelbase=2.57, cg_front_axle=1.208, cg_rear_axle=1.362, cg_height=0.46, mass=1222, inertia=1222, length=4.24, width=1.775, wheel_diameter=0.5285, wheel_width=0.15))
world.add_component(car, com.Engine(torque_curve=torque_curve, idle=700, rev_limit=7499, rpm=2000, throttle = 0))
world.add_component(car, com.GearBox(4.100, -3.437, 3.626, 2.188, 1.541, 1.213, 1.000, 0.767, clutch_rpm=0))
world.add_component(car, com.DeltaTime(dt=0))
world.add_component(car, com.ForwardForce(forward_force=0))
img = pygame.image.load("assets/car_black_5.png")
world.add_component(car, com.Sprite(sprite=img))
world.add_component(car, com.Steering(angle=0))
world.add_component(car, com.Direction(initV=([0,1])))
world.add_component(car, com.Acceleration(initV=[0, 0]))
#world.add_component(car, com.Temp(v=0,t=0))
#world.add_processor(pro.BigProcessor())
world.add_processor(pro.CarAccelerationProcessor())
world.add_processor(pro.CarVelocityProcessor())
world.add_processor(pro.CarPositionProcessor())
world.add_processor(pro.WeightTransferProcessor())
world.add_processor(pro.DriveForceProcessor())
world.add_processor(pro.RPMProcessor(), priority=1)
world.add_processor(pro.ClutchProcessor())
#world.add_processor(pro.AngluarProcessor())

#world.add_processor(pro.SteeringProcessor())
world.add_processor(pro.RenderProcessor(renderer=screen), priority=1)

def gameLoop():
    # Framerate clock
    last_time = time.time()
    clock = pygame.time.Clock()

    # Run until the user asks to quit
    running = True
    pos = 0

    while running:
        print(world.component_for_entity(car, com.ForwardForce).forward_force)
        #print(world.component_for_entity(car, com.Velocity).velV.magnitude()*3.6)
        # Input
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
                if pygame.joystick.Joystick(0).get_button(0) == True:
                    world.component_for_entity(car, com.GearBox).clutch = True
                #Handbreak
                #print(pygame.joystick.Joystick(0).get_button(1))
            if event.type == pygame.JOYBUTTONUP:
                #Gear down
                #print(pygame.joystick.Joystick(0).get_button(4))
                #Gear up
                #print(pygame.joystick.Joystick(0).get_button(5))
                #Clutch
                if pygame.joystick.Joystick(0).get_button(0) == False:
                    world.component_for_entity(car, com.GearBox).clutch = False
                #Handbreak
                #print(pygame.joystick.Joystick(0).get_button(1))
            if event.type == pygame.JOYAXISMOTION:
                #UP and LEFT is negative
                #Steering

                if pygame.joystick.Joystick(0).get_axis(0) < -0.2:
                    world.component_for_entity(car, com.Steering).angle = (pygame.joystick.Joystick(0).get_axis(0)*1.25 + 0.25)*-35
                elif pygame.joystick.Joystick(0).get_axis(0) > 0.2:
                    world.component_for_entity(car, com.Steering).angle = (pygame.joystick.Joystick(0).get_axis(0)*1.25 - 0.25)*-35
                else:
                    world.component_for_entity(car, com.Steering).angle = 0

                #Throttle
                #print("RT = " + str(pygame.joystick.Joystick(0).get_axis(5)))
                if pygame.joystick.Joystick(0).get_axis(5) >= -0.99:
                    world.component_for_entity(car, com.Engine).throttle = (pygame.joystick.Joystick(0).get_axis(5) - constants.OLD_ZAXIS_MIN) * constants.RANGE_RATIO
                if pygame.joystick.Joystick(0).get_axis(5) < -0.99:
                    world.component_for_entity(car, com.Engine).throttle = 0

                #Goes from -1.0 to 1.0
                #Break
                #print("LT = " + str(pygame.joystick.Joystick(0).get_axis(4)))
        
        # Delta time to make sure everything runs as if its always 60 FPS

        dt = time.time() - last_time
        last_time = time.time()
        dt = dt * constants.TARGET_FRAMERATE
        world.component_for_entity(car, com.DeltaTime).dt = dt
        
        # Background color
        screen.fill((255, 255, 255))
        # Update the game
        world.process()


        # Test circle
        #pygame.draw.circle(screen, (0, 0, 255), (pos, 250), 75)

        # Updates display
        pygame.display.update()
        clock.tick(constants.TARGET_FRAMERATE)


gameLoop()

# Quit
#pygame.joystick.quit()
pygame.quit()
