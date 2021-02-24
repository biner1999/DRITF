
import esper
import pygame
import components as com
import constants


class CarAccelerationProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity):
            accel.accV.x = ((dire.dirV.x * 500) - (constants.DRAG_COEFF * velo.velV.magnitude() * velo.velV.x) - (constants.RR_FORCE * velo.velV.x)) / 1222
            accel.accV.y = ((dire.dirV.y * 500) - (constants.DRAG_COEFF * velo.velV.magnitude() * velo.velV.y) - (constants.RR_FORCE * velo.velV.y)) / 1222


class CarVelocityProcessor(esper.Processor):

    def process(self):
        for ent, (dt, accel, velo) in self.world.get_components(com.DeltaTime, com.Acceleration, com.Velocity):
            velo.velV.x += accel.accV.x * dt.dt
            velo.velV.y += accel.accV.y * dt.dt


class CarPositionProcessor(esper.Processor):

    def process(self):
        for ent, (dt, velo, pos) in self.world.get_components(com.DeltaTime, com.Velocity, com.Position):
            pos.posV.x += velo.velV.x * dt.dt
            pos.posV.y += velo.velV.y * dt.dt


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
        for ent, (spd, whe, grs, box) in self.world.get_components(com.Speed, com.Wheel, com.GearRatios, com.GearBox):
            #spd.speed = (RPM*whe.diameter / (grs.rear_diff * grs.current_gear * 336)
            pass