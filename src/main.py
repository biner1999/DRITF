#Importing and initializing PyGame
#
import pygame
from pygame.locals import *
from pygame.joystick import *
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()

#Set up a window and a window resolution
pygame.display.set_caption("DRITF!")
win_res = (500, 500)
screen = pygame.display.set_mode(win_res,0,32)

# Run until the user asks to quit
running = True

while running:


    #Checks if user presses the X button to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                pass
    

    print(pygame.joystick.get_axis(1))



    #Background color
    screen.fill((255, 255, 255))


    #Test circle
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)


    #Updates display
    pygame.display.update()
    clock.tick(60)


#Quit
pygame.joystick.quit
pygame.quit()
