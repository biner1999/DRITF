
import esper
import pygame
import components as com
import constants


class CarAccelerationProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff, eng) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce, com.Engine):
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

class DriveForceProcessor(esper.Processor):

    def process(self):
        for ent, (cha, eng, grb, ff) in self.world.get_components(com.Chassis, com.Engine, com.GearBox, com.ForwardForce):
            #ff.forward_force = (eng.torque_curve[3000] * grb.current_gear * grb.rear_diff) * cha.wheel_diameter/2 * throttle
            #ff.forward_force = (eng.current_torque * throttle * grb.current_gear * grb.rear_diff) * (cha.wheel_diameter/2)
            #ff.forward_force = (eng.torque_curve[700-700] * 3.6 * grb.rear_diff) * cha.wheel_diameter/2 * 1
            ff.forward_force = (eng.torque_curve[eng.rpm-eng.idle] * eng.throttle * grb.rear_diff * grb.gear_ratios[grb.current_gear])/(cha.wheel_diameter/2)


class RPMProcessor(esper.Processor):
    def process(self):
        for ent, (eng, grb, cha, velo) in self.world.get_components(com.Engine, com.GearBox, com.Chassis, com.Velocity):
            eng.rpm = int((velo.velV.magnitude()/(cha.wheel_diameter/2)) * grb.rear_diff * grb.gear_ratios[grb.current_gear] * constants.RADS_to_RPM)
            if eng.rpm < eng.idle:
                eng.rpm = eng.idle
            if eng.rpm > eng.rev_limit:
                eng.rpm = eng.rev_limit
                
class AngluarProcessor(esper.Processor):
    def process(self):
        for ent, (eng, grb, cha, dt) in self.world.get_components(com.Engine, com.GearBox, com.Chassis, com.DeltaTime):
            inertia = 2 * 15 * (cha.wheel_diameter/2)**2
            ang_acc = (eng.torque_curve[eng.rpm-eng.idle] * eng.throttle * grb.rear_diff * grb.gear_ratios[grb.current_gear]) / inertia
            ang_vel += ang_acc * dt.dt


"""
class RPMProcessor(esper.Processor):

    def process(self):
        for ent, (eng, grb, dt, velo, cha) in self.world.get_components(com.Engine, com.GearBox, com.DeltaTime, com.Velocity, com.Chassis):
            if grb.clutch == False:
                # Engine inertia and we assign engine RPM to a seperate variable
                eng_inertia = 0.5 * 9.34 * 0.16**2 # 0.5 * mass * radius^2
                temp_rpm = eng.rpm

                # We calculate the RPM from flywheel speed and increment it by that, also check if it is within the engine limit
                flywheel_acc = (eng.torque_curve[int(eng.rpm)-701] - ((temp_rpm - eng.idle)/60)) / eng_inertia * constants.RADS_to_RPM # Engine Tq - Engine Breaking Tq (linear curve for now)
                temp_rpm += flywheel_acc * dt.dt
                if temp_rpm > eng.rev_limit:
                    eng.rpm = eng.rev_limit
                elif temp_rpm < eng.idle:
                    eng.rpm = eng.idle
                else:
                    eng.rpm = temp_rpm
                
                # Calculate engine momentum
                eng_momentum = eng_inertia * eng.rpm * constants.RPM_to_RADS

                # Trans inertia
                trans_inertia = 1.5
                # Get clutch RPM from wheel speed
                grb.clutch_rpm = (velo.velV.magnitude() * grb.rear_diff * 3.6) / (cha.wheel_diameter/2) * constants.RADS_to_RPM
                
                #temp_clutch_rpm = grb.clutch_rpm
                #clutch_acc = (velo.velV.magnitude() * grb.rear_diff * grb.gear_ratio) / (cha.wheel_diameter/2) * constants.RADS_to_RPM
                #temp_clutch_rpm += clutch_acc * dt.dt
                #grb.clutch_rpm = temp_clutch_rpm

                # Calculate trans momentum
                trans_momentum = trans_inertia * grb.clutch_rpm * constants.RPM_to_RADS

            else:
                fly_clutch_speed = (eng_momentum + trans_momentum)/(eng_inertia + trans_inertia)
                wheel_speed = (fly_clutch_speed * constants.RADS_to_RPM * cha.wheel_diameter/2) / (grb.rear_diff * grb.gear_ratio) * constants.RPM_to_RADS
"""

class ClutchProcessor(esper.Processor):

    def process(self):
        for ent, (eng, velo, cha, grb) in self.world.get_components(com.Engine, com.Velocity, com.Chassis, com.GearBox):
            pass

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
