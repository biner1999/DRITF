import math

import esper
import pygame
from components import components as com
from other import constants

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

    def __init__(self, renderer, car):
        super().__init__()
        self.renderer = renderer
        self.car = car
    
    def process(self):
        s = pygame.Surface((500, 250), pygame.SRCALPHA)
        s.fill((0,0,0,80))
        self.renderer.blit(s, (self.renderer.get_width()-500, self.renderer.get_height()-250))
        a = pygame.Rect(1440, 900, 500, 220)
        pygame.draw.arc(self.renderer, (215, 108, 0), a, 0.5, 2.64, 30)
        pygame.draw.arc(self.renderer, (165, 0, 0), a, 0.5, 1, 30)

        oldr = self.world.component_for_entity(self.car, com.Engine).rev_limit
        newr = 0.5-2.64
        newv = (((self.world.component_for_entity(self.car, com.Engine).rpm)*newr)/oldr) + 2.64
        pygame.draw.arc(self.renderer, (255, 178, 0), a, newv, 2.64, 30)


class Gear(esper.Processor):
    def __init__(self, gear):
        super().__init__()
        self.gear = gear

    def process(self):
        for ent, (grbox) in self.world.get_component(com.GearBox):
            gear_no = grbox.current_gear
            if gear_no == 0:
                gear = "R"
            elif gear_no == 1:
                gear = "N"
            else:
                gear = str(gear_no - 1)
            
            self.world.component_for_entity(self.gear, com.Text).text = gear

class Speed(esper.Processor):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed

    def process(self):
        for ent, (spd) in self.world.get_component(com.Velocity):
            self.world.component_for_entity(self.speed, com.Text).text = str(int(spd.velV.magnitude()*3.6))

class TotalPointsCalculaton(esper.Processor):
    
    def process(self):
        for ent, (points, txt) in self.world.get_components(com.TotalPoints, com.Text):

            txt.text = "{:,}".format(points.points)

class SinglePointsCalculaton(esper.Processor):
    
    def process(self):
        for ent, (points, txt) in self.world.get_components(com.SinglePoints, com.Text):

            txt.text = ("+" + "{:,}".format(points.points))

class Timer(esper.Processor):

    def process(self):
        for ent, (tme, dt, txt) in self.world.get_components(com.Time, com.DeltaTime, com.Text):
            tme.time -= dt.dt
            txt.text = str(math.ceil(tme.time))
            if tme.time <= 0:
                self.world.component_for_entity(19, com.States).current_state = "menu" # Turn the loop off