
import esper
import pygame
import components as com

class MovementProcessor(esper.Processor):

    def process(self):
        for ent, (dt, vel, pos) in self.world.get_components(com.DeltaTime, com.Velocity, com.Position):
            pos.x += vel.x * dt.dt
            pos.y += vel.y * dt.dt


class RenderProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (spr, pos, stre) in self.world.get_components(com.Sprite, com.Position, com.Steering):
            rot_spr = pygame.transform.rotate(spr.sprite, stre.angle)
            self.renderer.blit(rot_spr, [pos.x, pos.y])
            
class SteeringProcessor(esper.Processor):

    def process(self):
        for ent, (spr, stre) in self.world.get_components(com.Sprite, com.Steering):
            spr.sprite = pygame.transform.rotate(spr.sprite, stre.angle)