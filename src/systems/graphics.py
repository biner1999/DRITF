
import math

import esper
import pygame

from components import components as com
from other import constants

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
            #         pygame.draw.rect(self.renderer, (0,color,0), value)

class CameraProcessor(esper.Processor):

    def __init__(self, renderer, car):
        super().__init__()
        self.renderer = renderer
        self.car = car

    def process(self):
        car_pos = self.world.component_for_entity(self.car, com.Position).posV*constants.SCALE
        sprite = self.world.component_for_entity(self.car, com.Sprite).sprite
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

    def __init__(self, renderer, car, tilemap):
        super().__init__()
        self.renderer = renderer
        self.car = car
        self.tilemap = tilemap

    def process(self):
        cam = self.world.component_for_entity(self.tilemap, com.Camera)
        car_pos = self.world.component_for_entity(self.car, com.Position).posV*constants.SCALE
        for ent, (spr, pos, stre, col) in self.world.get_components(com.Sprite, com.Position, com.Steering, com.ObjectCollisions):
            rot_spr = pygame.transform.rotate(spr.sprite, math.degrees(stre.heading)-180)
            rot_rect = rot_spr.get_rect(center = spr.sprite.get_rect(topleft = [pos.posV.x*constants.SCALE-cam.posV.x, pos.posV.y*constants.SCALE-cam.posV.y]).center)
            col.rect = rot_spr.get_rect()

            self.renderer.blit(rot_spr, rot_rect)

            #pygame.draw.rect(self.renderer, (255, 0, 0), [car_pos.x-35, car_pos.y-60, 70, 120])

            #ms = pygame.mask.from_surface(rot_spr)
            #msr = ms.outline()
            #pygame.draw.polygon(self.renderer,(200,150,150),msr, 0)
            #radius = math.sqrt(spr.sprite.get_rect().center[0]**2 + spr.sprite.get_rect().center[1]**2)-15
            #x = radius*math.sin(math.pi+0.4+stre.heading)
            #y = radius*math.cos(math.pi+0.4+stre.heading)

            #a = pygame.Rect(x+pos.posV.x-cam.posV.x+30, y+pos.posV.y-cam.posV.y+55, 10, 10)
            #pygame.draw.rect(self.renderer, (255,0,0), a)

class RenderObjectsProcessor(esper.Processor):

    def __init__(self, renderer, tilemap):
        super().__init__()
        self.renderer = renderer
        self.tilemap = tilemap

    def process(self):
        cam = self.world.component_for_entity(self.tilemap, com.Camera)
        for ent, (spr, loc, ang, col) in self.world.get_components(com.Sprite, com.Location, com.Angle, com.ObjectCollisions):
            rot_spr = pygame.transform.rotate(spr.sprite, ang.angle)
            rot_rect = rot_spr.get_rect(center = spr.sprite.get_rect(topleft = [loc.x-cam.posV.x, loc.y-cam.posV.y]).center)
            col.rect = rot_spr.get_rect()
            col.rect.x = loc.x-cam.posV.x
            col.rect.y = loc.y-cam.posV.y
            self.renderer.blit(rot_spr, rot_rect)
