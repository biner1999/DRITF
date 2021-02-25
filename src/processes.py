
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

class WeightTransferProcessor(esper.Processor):

    def process(self):
        for ent, (chas, accel) in self.world.get_components(com.Chassis, com.Acceleration):
            chas.weight_front_dynamic = chas.weight_front_standstill - (chas.cg_height/chas.wheelbase)*chas.mass*accel.accV.magnitude()
            chas.weight_rear_dynamic = chas.weight_rear_standstill + (chas.cg_height/chas.wheelbase)*chas.mass*accel.accV.magnitude()

class RenderProcessor(esper.Processor):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer

    def process(self):
        for ent, (spr, pos, stre) in self.world.get_components(com.Sprite, com.Position, com.Steering):
            rot_spr = pygame.transform.rotate(spr.sprite, stre.angle)
            self.renderer.blit(rot_spr, [pos.posV.x, pos.posV.y])






class XXXProcessor(esper.Processor):

    def process(self):
        for ent, () in self.world.get_components():
            pass
