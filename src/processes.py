
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

class CollisionsProcessor(esper.Processor):
    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (rect) in self.world.get_component(com.Rect):
            for ent, (tmcol) in self.world.get_component(com.TileMapCollisions):
                hit_list = []
                #pygame.draw.rect(self.renderer, (255, 0, 0), rect.rect)
                for tile in tmcol.rects["layer1"]:
                    #pygame.draw.rect(self.renderer, (0, 255, 0), tile)
                    if rect.rect.colliderect(tile):
                        hit_list.append(tile)
                print(hit_list)

class XXXProcessor(esper.Processor):

    def process(self):
        for ent, () in self.world.get_components():
            pass
