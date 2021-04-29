import esper
import pygame
import components as com
import constants
import numpy as np
import math
import pytmx
import random
import time
from collections import defaultdict

class DisplayBoxText(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (txt, surf, loc) in self.world.get_components(com.Text, com.Surface, com.Location):
            background = pygame.Surface((surf.width, surf.height), pygame.SRCALPHA)
            background.fill(surf.color)
            self.renderer.blit(background, (loc.x, loc.y))
            if txt.alignment == 1:
                self.drawTextLeft(txt.font, txt.text, (255, 255, 255), self.renderer, loc.x+background.get_width()/10, loc.y+background.get_height()/2)
            if txt.alignment == 2:
                self.drawTextCentred(txt.font, txt.text, (255, 255, 255), self.renderer, loc.x+background.get_width()/2, loc.y+background.get_height()/2)

    
    def drawTextCentred(self, font, text, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        surface.blit(textobj, (x - textrect.width/2, y - textrect.height/2))

    def drawTextLeft(self, font, text, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        surface.blit(textobj, (x, y - textrect.height/2))

class Speedometer(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer
    
    def process(self):
        s = pygame.Surface((500, 250), pygame.SRCALPHA)
        s.fill((0,0,0,80))
        self.renderer.blit(s, (self.renderer.get_width()-500, self.renderer.get_height()-250))
        a = pygame.Rect(1440, 900, 500, 220)
        pygame.draw.arc(self.renderer, (215, 108, 0), a, 0.5, 2.64, 30)
        pygame.draw.arc(self.renderer, (165, 0, 0), a, 0.5, 1, 30)

        oldr = self.world.component_for_entity(1, com.Engine).rev_limit
        newr = 0.5-2.64
        newv = (((self.world.component_for_entity(1, com.Engine).rpm)*newr)/oldr) + 2.64
        pygame.draw.arc(self.renderer, (255, 178, 0), a, newv, 2.64, 30)


class Gear(esper.Processor):
    def process(self):
        for ent, (grbox) in self.world.get_component(com.GearBox):
            gear_no = grbox.current_gear
            if gear_no == 0:
                gear = "R"
            elif gear_no == 1:
                gear = "N"
            else:
                gear = str(gear_no - 1)
            
            self.world.component_for_entity(7, com.Text).text = gear

class Speed(esper.Processor):
    def process(self):
        for ent, (spd) in self.world.get_component(com.Velocity):
            self.world.component_for_entity(6, com.Text).text = str(int(spd.velV.magnitude()*3.6))

class PointsCalculaton(esper.Processor):
    
    def process(self):
        for ent, (points, txt) in self.world.get_components(com.Points, com.Text):
            points.points = 10000000

            txt.text = "{:,}".format(points.points)