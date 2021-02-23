
import esper
import pygame
import components as com

class MovementProcessor(esper.Processor):

    def process(self):
        for ent, (dt, velo, pos, dire) in self.world.get_components(com.DeltaTime, com.Velocity, com.Position, com.DirVector):
            pos.posV += dire.dirV * velo.vel * dt.dt


class RenderProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (spr, pos, stre) in self.world.get_components(com.Sprite, com.Position, com.Steering):
            rot_spr = pygame.transform.rotate(spr.sprite, stre.angle)
            self.renderer.blit(rot_spr, [pos.posV.x, pos.posV.y])
            
class SteeringProcessor(esper.Processor):

    def process(self):
        for ent, (spr, stre) in self.world.get_components(com.Sprite, com.Steering):
            spr.sprite = pygame.transform.rotate(spr.sprite, stre.angle)

class SpeedProcessor(esper.Processor):

    def process(self):
        for ent, (spd, tyre, grs, box) in self.world.get_components(com.Speed, com.Tyre, com.GearRatios, com.GearBox):
            spd.speed = (RPM*tyre.diameter / (grs.rear_diff * grs.current_gear * 336)