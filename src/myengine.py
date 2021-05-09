# Game related libraries
import pygame
from pygame.locals import *
from pygame.joystick import *
import myworld
import components as com
import constants
import math

class Engine():

    def __init__(self):
        # Intializations of PyGame modules
        pygame.init()
        pygame.font.init()
        pygame.joystick.Joystick(0).init()

        # Joystick
        self.joysticks = [pygame.joystick.Joystick(x) 
        for x in range(pygame.joystick.get_count())]

        # Set up a window and a window resolution
        pygame.display.set_caption("DRITF!")
        win_res = (1920, 1080)
        self.screen = pygame.display.set_mode(win_res,0,32)

        # Fonts
        #myfont = pygame.font.SysFont('Comic Sans MS', 100)
        #mysmallfont = pygame.font.SysFont('Comic Sans MS', 50)

        world = myworld.MyWorld(self.screen)

        running = True
        click = True
        clock = pygame.time.Clock()

        while running:
            # Inputs
            loaded_state = world.world.component_for_entity(19, com.States).loaded_state
            if loaded_state == "game":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RIGHT:
                            pass
                    if event.type == pygame.JOYBUTTONDOWN:
                        #Go back to main menu
                        if pygame.joystick.Joystick(0).get_button(7):
                            pass
                            # running = False BACK TO MENU INSTEAD
                        #Gear down
                        if pygame.joystick.Joystick(0).get_button(4):
                            if world.world.component_for_entity(1, com.GearBox).current_gear > 0:
                                world.world.component_for_entity(1, com.GearBox).current_gear -= 1
                                #print(world.world.component_for_entity(1, com.GearBox).current_gear)

                        #Gear up
                        if pygame.joystick.Joystick(0).get_button(5):
                            if world.world.component_for_entity(1, com.GearBox).current_gear < world.world.component_for_entity(1, com.GearBox).no_of_gears-1:
                                world.world.component_for_entity(1, com.GearBox).current_gear += 1
                                #print(world.world.component_for_entity(1, com.GearBox).current_gear)
                        #Clutch
                        if pygame.joystick.Joystick(0).get_button(0):
                            world.world.component_for_entity(1, com.GearBox).clutch = True
                        #Handbreak
                        if pygame.joystick.Joystick(0).get_button(1):
                            world.world.component_for_entity(1, com.Chassis).ebrake = 1
                    if event.type == pygame.JOYBUTTONUP:
                        #Clutch
                        if not pygame.joystick.Joystick(0).get_button(0):
                            world.world.component_for_entity(1, com.GearBox).clutch = False
                        #Handbreak
                        if not pygame.joystick.Joystick(0).get_button(1):
                            world.world.component_for_entity(1, com.Chassis).ebrake = 0
                    if event.type == pygame.JOYAXISMOTION:
                        #UP and LEFT is negative
                        #Steering
                        if pygame.joystick.Joystick(0).get_axis(0) < -0.2:
                            world.world.component_for_entity(1, com.Steering).steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 + 0.25)*-world.world.component_for_entity(1, com.Steering).max_angle[0])
                        elif pygame.joystick.Joystick(0).get_axis(0) > 0.2:
                            world.world.component_for_entity(1, com.Steering).steer_angle = math.radians((pygame.joystick.Joystick(0).get_axis(0)*1.25 - 0.25)*-world.world.component_for_entity(1, com.Steering).max_angle[0])
                        else:
                            world.world.component_for_entity(1, com.Steering).steer_angle = 0
                        #Throttle
                        #print("RT = " + str(pygame.joystick.Joystick(0).get_axis(5)))
                        if pygame.joystick.Joystick(0).get_axis(5) >= -0.99:
                            world.world.component_for_entity(1, com.Engine).throttle = (pygame.joystick.Joystick(0).get_axis(5) - constants.OLD_ZAXIS_MIN) * constants.RANGE_RATIO
                        if pygame.joystick.Joystick(0).get_axis(5) < -0.99:
                            world.world.component_for_entity(1, com.Engine).throttle = 0

                        #Goes from -1.0 to 1.0
                        #Break
                        #print("LT = " + str(pygame.joystick.Joystick(0).get_axis(2)))
                        if pygame.joystick.Joystick(0).get_axis(2) >= -0.99:
                            world.world.component_for_entity(1, com.Chassis).brake = (pygame.joystick.Joystick(0).get_axis(2) - constants.OLD_ZAXIS_MIN) * constants.RANGE_RATIO
                        if pygame.joystick.Joystick(0).get_axis(2) < -0.99:
                            world.world.component_for_entity(1, com.Chassis).brake = 0
            elif loaded_state == "menu" or loaded_state == "tuning":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = True
                # or
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    click = pygame.mouse.get_pressed()[0]
                mx, my = pygame.mouse.get_pos()
            world.world.process()
            pygame.display.update()
            clock.tick(constants.TARGET_FRAMERATE)
            click = False
            #print(world.world._processors)
"""
                if play_button.collidepoint((mx, my)):
                    if click:
                        gameLoop()
                if modify_button.collidepoint((mx, my)):
                    if click:
                        modifyLoop()
"""




