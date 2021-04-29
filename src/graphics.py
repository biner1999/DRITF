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

class TileMapProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer
    
    def process(self):
        for ent, (tm, cam, col) in self.world.get_components(com.TileMap, com.Camera, com.TileMapCollisions):
            col.rects.clear()
            for i in range(len(tm.tilemap.layers)):
                layer_name = tm.tilemap.layers[i].name
                #tm.rects_dict[layer_name] = []
            for layer in tm.tilemap.layers:
                for x, y, image in layer.tiles():
                    self.renderer.blit(image, [x*tm.tilemap.tilewidth-cam.posV.x, y*tm.tilemap.tileheight-cam.posV.y])
                    col.rects[layer.name].append(pygame.Rect(x*tm.tilemap.tilewidth, y*tm.tilemap.tileheight, tm.tilemap.tilewidth, tm.tilemap.tileheight))
                    #tm.rects.append(pygame.Rect(x*tm.tilemap.tilewidth, y*tm.tilemap.tileheight, tm.tilemap.tilewidth, tm.tilemap.tileheight))
                    tm.rects_dict[layer.name].append(pygame.Rect(x*tm.tilemap.tilewidth, y*tm.tilemap.tileheight, tm.tilemap.tilewidth, tm.tilemap.tileheight))
            #for i in range(len(tm.rects)):
            #    pygame.draw.rect(self.renderer, (0, 255, 0), (tm.rects[i].x, tm.rects[i].y, tm.rects[i].width, tm.rects[i].height))
            #color = 0
            #for key in tm.rects_dict:
            #    color += 100
            #    for value in tm.rects_dict[key]:
            #
            #         pygame.draw.rect(self.renderer, (0,color,0), value)

class CameraProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        car_pos = self.world.component_for_entity(1, com.Position).posV*28
        sprite = self.world.component_for_entity(1, com.Sprite).sprite
        for ent, (tm, cam) in self.world.get_components(com.TileMap, com.Camera):
            tx = cam.posV.x
            ty = cam.posV.y
            cam.posV.x += car_pos.x - cam.posV.x - cam.offset_x + sprite.get_width()/2
            cam.posV.y += car_pos.y - cam.posV.y - cam.offset_y + sprite.get_height()/2
            if cam.posV.x < 0:
                cam.posV.x = 0
            if cam.posV.y < 0:
                cam.posV.y = 0
            if cam.posV.y > tm.tilemap.tileheight*tm.tilemap.height - self.renderer.get_height():
                cam.posV.y = tm.tilemap.tileheight*tm.tilemap.height - self.renderer.get_height()
            if cam.posV.x > tm.tilemap.tilewidth*tm.tilemap.width - self.renderer.get_width():
                cam.posV.x = tm.tilemap.tilewidth*tm.tilemap.width - self.renderer.get_width()

class RenderProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        cam = self.world.component_for_entity(2, com.Camera)
        car_pos = self.world.component_for_entity(1, com.Position).posV*28
        for ent, (spr, pos, stre, col) in self.world.get_components(com.Sprite, com.Position, com.Steering, com.ObjectCollisions):
            rot_spr = pygame.transform.rotate(spr.sprite, math.degrees(stre.heading)-180)
            rot_rect = rot_spr.get_rect(center = spr.sprite.get_rect(topleft = [pos.posV.x*28-cam.posV.x, pos.posV.y*28-cam.posV.y]).center)
            col.rect = rot_spr.get_rect()

            self.renderer.blit(rot_spr, rot_rect)

            #pygame.draw.rect(self.renderer, (255, 0, 0), [car_pos.x, car_pos.y, 70, 120])

            #ms = pygame.mask.from_surface(rot_spr)
            #msr = ms.outline()
            #pygame.draw.polygon(self.renderer,(200,150,150),msr, 0)
            #radius = math.sqrt(spr.sprite.get_rect().center[0]**2 + spr.sprite.get_rect().center[1]**2)-15
            #x = radius*math.sin(math.pi+0.4+stre.heading)
            #y = radius*math.cos(math.pi+0.4+stre.heading)

            #a = pygame.Rect(x+pos.posV.x-cam.posV.x+30, y+pos.posV.y-cam.posV.y+55, 10, 10)
            #pygame.draw.rect(self.renderer, (255,0,0), a)


