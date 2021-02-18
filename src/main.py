# Imports
import pygame, sys, time
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

pos = 0

# Framerate clock
last_time = time.time()
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:

    dt = time.time() - last_time
    last_time = time.time()
    dt = dt * constants.TARGET_FRAMERATE
    pos += 1 * dt

    # Checks if user presses the X button to close the window
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
            print("LS L/R = " + str(pygame.joystick.Joystick(0).get_axis(0)))
            #Goes from -1.0 to 1.0
            #Break
            print("LT = " + str(pygame.joystick.Joystick(0).get_axis(4)))
            #Throttle
            print("RT = " + str(pygame.joystick.Joystick(0).get_axis(5)))
    

    # Background color
    screen.fill((255, 255, 255))

    # Test circle
    pygame.draw.circle(screen, (0, 0, 255), (pos, 250), 75)

    # Updates display
    pygame.display.update()
    clock.tick(constants.TARGET_FRAMERATE)


# Quit
pygame.joystick.quit()
pygame.quit()
