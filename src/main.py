# Imports
import pygame
import sys
import time
import esper
import components as com
import processes as pro


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


car = world.create_entity()
world.add_component(car, com.Position(x=0, y=250))
world.add_component(car, com.Velocity(x=1,y=0))
world.add_component(car, com.DeltaTime(dt=0))
img = pygame.image.load("assets/car_black_5.png")
world.add_component(car, com.Sprite(sprite=img))
world.add_component(car, com.Steering(angle=0))
#world.add_component(car, com.Sprite(sprite="car.png"))

world.add_processor(pro.MovementProcessor())
#world.add_processor(pro.SteeringProcessor())
world.add_processor(pro.RenderProcessor(renderer=screen))


def gameLoop():
    # Framerate clock
    last_time = time.time()
    clock = pygame.time.Clock()

    # Run until the user asks to quit
    running = True
    pos = 0

    while running:

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    pass
            if event.type == pygame.JOYBUTTONDOWN:
                #Gear down
                print(pygame.joystick.Joystick(0).get_button(4))
                #Gear up
                print(pygame.joystick.Joystick(0).get_button(5))
                #Clutch
                print(pygame.joystick.Joystick(0).get_button(0))
                #Handbreak
                print(pygame.joystick.Joystick(0).get_button(1))
            if event.type == pygame.JOYBUTTONUP:
                #Gear down
                print(pygame.joystick.Joystick(0).get_button(4))
                #Gear up
                print(pygame.joystick.Joystick(0).get_button(5))
                #Clutch
                print(pygame.joystick.Joystick(0).get_button(0))
                #Handbreak
                print(pygame.joystick.Joystick(0).get_button(1))
            if event.type == pygame.JOYAXISMOTION:
                #UP and LEFT is negative
                #Steering
                #print("LS L/R = " + str(pygame.joystick.Joystick(0).get_axis(0)))
                if pygame.joystick.Joystick(0).get_axis(0) < -0.2:
                    world.component_for_entity(car, com.Steering).angle = (pygame.joystick.Joystick(0).get_axis(0)*1.25 + 0.25)*-35
                elif pygame.joystick.Joystick(0).get_axis(0) > 0.2:
                    world.component_for_entity(car, com.Steering).angle = (pygame.joystick.Joystick(0).get_axis(0)*1.25 - 0.25)*-35
                else:
                    world.component_for_entity(car, com.Steering).angle = 0
                
                #Goes from -1.0 to 1.0
                #Break
                #print("LT = " + str(pygame.joystick.Joystick(0).get_axis(4)))
                #Throttle
                #print("RT = " + str(pygame.joystick.Joystick(0).get_axis(5)))
        
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
