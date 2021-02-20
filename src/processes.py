
import esper
import pygame
import components as c

class MovementProcessor(esper.Processor):

    def process(self):
        for ent, (dt, vel, pos) in self.world.get_components(c.DeltaTime, c.Velocity, c.Position):
            pos.x += vel.x * dt.dt
            pos.y += vel.y * dt.dt


class RenderProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (spr, pos) in self.world.get_components(c.Sprite, c.Position):
            self.renderer.blit(spr.sprite, [pos.x, pos.y])
            