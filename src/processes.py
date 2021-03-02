
import esper
import pygame
import components as com
import constants


class CarAccelerationProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce):
            accel.accV.x = ((dire.dirV.x * ff.forward_force) - (constants.DRAG_COEFF * velo.velV.magnitude() * velo.velV.x) - (constants.RR_FORCE * velo.velV.x)) / 1222
            accel.accV.y = ((dire.dirV.y * ff.forward_force) - (constants.DRAG_COEFF * velo.velV.magnitude() * velo.velV.y) - (constants.RR_FORCE * velo.velV.y)) / 1222


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

class EngineForceProcessor(esper.Processor):

    def process(self):
        for ent, (cha, eng, grb, ff) in self.world.get_components(com.Chassis, com.Engine, com.GearBox, com.ForwardForce):
            #ff.forward_force = (eng.torque_curve[3000] * grb.current_gear * grb.rear_diff) * cha.wheel_diameter/2 * throttle
            ff.forward_force = (eng.torque_curve[700-701] * 0.5 * 4.1) * cha.wheel_diameter/2 * 1



class RPMProcessor(esper.Processor):

    def process(self):
        for ent, (eng, grb, whe, dt) in self.world.get_components(com.Engine, com.GearBox, com.Wheel, com.DeltaTime):
            #rpm = wheel_rotation_rate * grb.current_gear * grb.rear_diff * 60 / 2 * 3.14
            #rpm = wheel_rotation_rate * 3.6 * 4.1 * (60/2*3.14)
            inertia = 0.5 * 9.34 * 0.16**2
            flywheel_acc = 100 / inertia / 60*2*3.14
            temp_rpm = eng.rpm
            temp_rpm += flywheel_acc * dt.dt
            if temp_rpm > eng.rev_limit:
                eng.rpm = eng.rev_limit
            elif temp_rpm < eng.idle:
                eng.rpm = eng.idle
            else:
                eng.rpm = temp_rpm


class SlipRatioProcessor(esper.Processor):

    def process(self):
        for ent, () in self.world.get_components():
            slip_ratio_x = (wheel_ang_vel*cha.wheel_diameter/2 - velo.velV.x) / velo.velV.magnitude()
            slip_ratio_y = (wheel_ang_vel*cha.wheel_diameter/2 - velo.velV.y) / velo.velV.magnitude()


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
