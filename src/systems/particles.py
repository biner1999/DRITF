import math
import random

import esper
import pygame
from components import components as com
from other import constants

class AddParticlesProcessor(esper.Processor):

    def __init__(self, car, tilemap):
        super().__init__()
        self.car = car
        self.tilemap = tilemap
    
    def process(self):
        
        car_pos = self.world.component_for_entity(self.car, com.Position).posV*constants.SCALE
        sprite = self.world.component_for_entity(self.car, com.Sprite).sprite
        car_ang = self.world.component_for_entity(self.car, com.Steering).heading
        cam_pos = self.world.component_for_entity(self.tilemap, com.Camera).posV
        car_sar = self.world.component_for_entity(self.car, com.Steering).sar

        if abs(car_sar) > 0.5:
            for ent, (par) in self.world.get_component(com.Particles):
                radius = math.sqrt(sprite.get_rect().center[0]**2 + sprite.get_rect().center[1]**2)-15

                x = radius*math.sin(math.pi+par.angle_offset+car_ang)
                y = radius*math.cos(math.pi+par.angle_offset+car_ang)

                x_src = int(x+car_pos.x-cam_pos.x+30)
                y_src = int(y+car_pos.y-cam_pos.y+55)

                for i in range(5):
                    r = random.randrange(110,150)
                    par.particles.append([[x_src, y_src], r, 200, car_ang])
        else:
            pass

class RenderParticlesProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer
    
    def process(self):
        for ent, (par) in self.world.get_component(com.Particles):
            for particle in par.particles:
                ang = particle[3]

                avdict = {0:4, 90:3, 180:4, 270:1}

                vert_vectors_pos = 0
                vert_vectors_neg = 0
                horz_vectors_pos = 0
                horz_vectors_neg = 0

                for key, value in avdict.items():
                    vert_vector = round(value*math.sin(math.radians(key) + ang), 4)
                    horz_vector = round(value*math.cos(math.radians(key) + ang), 4)
                    if vert_vector > 0:
                        vert_vectors_pos += vert_vector
                    elif vert_vector < 0:
                        vert_vectors_neg += vert_vector
                    if horz_vector > 0:
                        horz_vectors_pos += horz_vector
                    elif horz_vector < 0:
                        horz_vectors_neg += horz_vector
                        

                particle[0][1]-=random.randint(int(round(vert_vectors_neg)),int(round(vert_vectors_pos)))
                particle[0][0]+=random.randint(int(round(horz_vectors_neg)), int(round(horz_vectors_pos)))

                #i[1]-=random.randint(-1,3)
                #i[0]+=random.randint(-4, 4)
                #r = random.randrange(1,200)
                r = particle[1]
                particle[2] -= 2
                a = particle[2]
                if particle[0][1]<0 or a <= 0:
                    par.particles.remove(particle)
                else:
                    s = pygame.Surface((10, 10), pygame.SRCALPHA)
                    s.fill((r,r,r,a))
                    self.renderer.blit(s, (particle[0][0], particle[0][1]))