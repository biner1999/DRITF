# Imports
# General libraries

# Game related libraries
import pygame
from pygame.locals import *
from pygame.joystick import *
import esper

# My files
# ECS
from components import components as com
from systems import processes as pro
from systems import carphysics as carphys
from systems import graphics
from systems import gui
from systems import particles
# Other
from other import constants

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
"""

class BackgroundProcessor(esper.Processor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (bckgrnd) in self.world.get_component(com.Background):
            self.renderer.fill(bckgrnd.color)

class ButtonProcessor(esper.Processor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (rect, txt, clr, btn) in self.world.get_components(com.Rect, com.Text, com.Color, com.Button):
            if btn.state == self.world.component_for_entity(19, com.States).loaded_state:
                pygame.draw.rect(self.renderer, clr.color, rect.rect)
                self.drawTextCentred(txt.font, txt.text, (0, 0, 0), self.renderer, (rect.rect.x + rect.rect.width/2), (rect.rect.y + rect.rect.height/2))
                click = pygame.mouse.get_pressed()[0]
                mx, my = pygame.mouse.get_pos()
                if rect.rect.collidepoint((mx, my)):
                    if click:
                        self.world.component_for_entity(19, com.States).current_state = btn.goto_state


    def drawTextCentred(self, font, text, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        surface.blit(textobj, (x - textrect.width/2, y - textrect.height/2))

class SliderProcessor(esper.Processor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer
    
    def process(self):
        for ent, (sldr, txt) in self.world.get_components(com.Slider, com.Text):
            click = pygame.mouse.get_pressed()[0]
            mx, my = pygame.mouse.get_pos()

            slider_bar = pygame.Rect(sldr.bar_x, sldr.bar_y, sldr.bar_width, sldr.bar_height)
            pygame.draw.rect(self.renderer, sldr.bar_color, slider_bar)

            if slider_bar.collidepoint((mx,my)):
                if click:
                    sldr.slider_pos = mx
                    if mx < sldr.bar_x:
                        sldr.slider_pos = sldr.bar_x
                    elif mx > sldr.bar_x - sldr.slider_width + sldr.bar_width:
                        sldr.slider_pos = sldr.bar_x - sldr.slider_width + sldr.bar_width
                        
            slider_slider = pygame.Rect(sldr.slider_pos, sldr.bar_y, sldr.slider_width, sldr.bar_height)
            pygame.draw.rect(self.renderer, sldr.slider_color, slider_slider)
            actual_slider_pos = sldr.slider_pos - sldr.bar_x
            val = round(sldr.min_val + actual_slider_pos/sldr.interval, sldr.rounding)
            sldr.current_val[0] = val
            self.drawTextCentred(txt.font, str(sldr.current_val[0]), (0, 0, 0), self.renderer, self.renderer.get_width()/6*5, sldr.bar_y+sldr.bar_height/2)
            self.drawTextCentred(txt.font, txt.text, (0, 0, 0), self.renderer, self.renderer.get_width()/2, sldr.bar_y-25)

    def drawTextCentred(self, font, text, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        surface.blit(textobj, (x - textrect.width/2, y - textrect.height/2))