
import esper
import pygame
import components as com
import constants
import numpy as np
import math


class TestProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff, eng, grb, cha, dt, ster, caccel, cvelo, pos) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce, com.Engine, com.GearBox, com.Chassis, com.DeltaTime, com.Steering, com.CarAcceleration, com.CarVelocity, com.Position):
            str_ang = math.radians(ster.steer_angle)
            
            sn = math.sin(ster.heading)
            cs = math.cos(ster.heading)

            local_vx = cs * velo.velV.x + sn * velo.velV.y
            local_vy = cs * velo.velV.y - sn * velo.velV.x

            faw = cha.weight_front_standstill * constants.GRAVITY
            raw = cha.weight_rear_standstill * constants.GRAVITY

            yawSpeedFront = cha.cg_front_axle * ster.yawRate
            yawSpeedRear = -cha.cg_rear_axle * ster.yawRate

            slipAngleFront = math.atan2(local_vy + yawSpeedFront, abs(local_vx)) - np.sign(local_vx) * str_ang
            slipAngleRear  = math.atan2(local_vy + yawSpeedRear,  abs(local_vx))

            ster.fff = np.clip(-5*slipAngleFront, -2, 2) * faw
            ster.ffr = np.clip(-5*slipAngleRear, -2, 2) * raw
            
            # Calculates the engine RPM from speed
            eng.rpm = (abs(local_vx)/cha.wheel_radius) * (grb.rear_diff * abs(grb.gear_ratios[grb.current_gear])) * constants.RADS_to_RPM
            # Manages the idle RPM
            if eng.rpm < eng.idle:
                eng.rpm = eng.idle
                
            # Calculates the torque
            if eng.rpm >= eng.idle and eng.rpm < eng.rev_limit:
                eng.torque = eng.torque_curve[int(eng.rpm) - eng.idle]
            else:
                eng.torque = 0

            # Does not let RPM go over or under the rev limit
            if eng.rpm < eng.idle:
                eng.rpm = eng.idle
            elif eng.rpm > eng.rev_limit:
                eng.rpm = eng.rev_limit
            #print(eng.rpm)
            torque = (eng.throttle * eng.torque) * (grb.rear_diff * grb.gear_ratios[grb.current_gear])

            ff.forward_force = torque / cha.wheel_radius  - cha.brake*cha.brake_power*np.sign(local_vx)
            ff.sideway_force = 0

            drag_force_x = -constants.RR_COEFF * local_vx - constants.DRAG_COEFF * local_vx * abs(local_vx);
            drag_force_y = -constants.RR_COEFF * local_vy - constants.DRAG_COEFF * local_vy * abs(local_vy);

            total_force_x = ff.forward_force + drag_force_x
            total_force_y = ff.sideway_force + drag_force_y + math.cos(str_ang) * ster.fff + ster.ffr

            
            #print(velo.velV.y)
            local_ax = total_force_x / cha.mass
            local_ay = total_force_y / cha.mass

            accel.accV.x = cs * local_ax - sn * local_ay
            accel.accV.y = sn * local_ax + cs * local_ay

            velo.velV.x += accel.accV.x * dt.dt
            velo.velV.y += accel.accV.y * dt.dt

            pos.posV.x += velo.velV.x * dt.dt
            pos.posV.y += velo.velV.y * dt.dt

            angularTorque = ster.fff * cha.cg_front_axle - ster.ffr * cha.cg_rear_axle;

            if(velo.velV.magnitude() < 1 and eng.throttle == 0):
                velo.velV.y = 0
                velo.velV.x = 0
                angularTorque = 0
                yawRate = 0

            angularAccel = angularTorque / cha.inertia

            ster.yawRate += angularAccel * dt.dt
            if(velo.velV.magnitude() < 1 and str_ang < 0.05):
                ster.yawRate = 0
            ster.heading += ster.yawRate * dt.dt
class RPMTorqueProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff, eng, grb, cha, dt) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce, com.Engine, com.GearBox, com.Chassis, com.DeltaTime):
            # Calculates the engine RPM from speed
            eng.rpm = (abs(velo.velV.magnitude())/cha.wheel_radius) * (grb.rear_diff * abs(grb.gear_ratios[grb.current_gear])) * constants.RADS_to_RPM
            # Manages the idle RPM
            if eng.rpm < eng.idle:
                eng.rpm = eng.idle
                
            # Calculates the torque
            if eng.rpm >= eng.idle and eng.rpm < eng.rev_limit:
                eng.torque = eng.torque_curve[int(eng.rpm) - eng.idle]
            else:
                eng.torque = 0

            # Does not let RPM go over or under the rev limit
            if eng.rpm < eng.idle:
                eng.rpm = eng.idle
            elif eng.rpm > eng.rev_limit:
                eng.rpm = eng.rev_limit
            #print(eng.rpm)


class FForceProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff, eng, grb, cha, dt) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce, com.Engine, com.GearBox, com.Chassis, com.DeltaTime):
            # Calculates the wheel torque from engine torque and throttle
            torque = (eng.throttle * eng.torque) * (grb.rear_diff * grb.gear_ratios[grb.current_gear])

            ff.forward_force = torque / cha.wheel_radius
            ff.sideway_force = 0

class AccelerationProcessor(esper.Processor):

    def process(self):
        for ent, (ster, accel, caccel, dire, velo, cvelo, ff, eng, grb, cha, dt) in self.world.get_components(com.Steering, com.Acceleration, com.CarAcceleration, com.Direction, com.Velocity, com.CarVelocity, com.ForwardForce, com.Engine, com.GearBox, com.Chassis, com.DeltaTime):
            str_ang = math.radians(ster.steer_angle)
            
            # Resistance and total force as well as  acceleration

            drag_force_x = -constants.RR_COEFF * velo.velV.x - constants.DRAG_COEFF * velo.velV.x * velo.velV.magnitude();
            drag_force_y = -constants.RR_COEFF * velo.velV.y - constants.DRAG_COEFF * velo.velV.y * velo.velV.magnitude();

            total_force_x = ff.forward_force + drag_force_x - cha.brake*cha.brake_power*np.sign(velo.velV.x)
            total_force_y = ff.sideway_force + drag_force_y + math.cos(str_ang) * ster.fff + ster.ffr

            #print(total_force_x)
            
            #print(velo.velV.y)
            caccel.accV.x = total_force_x / cha.mass
            caccel.accV.y = total_force_y / cha.mass

            accel.accV.x = ster.cs * caccel.accV.x - ster.sn * caccel.accV.y
            accel.accV.y = ster.sn * caccel.accV.x + ster.cs * caccel.accV.y

class VelocityProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff, eng, grb, cha, dt) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce, com.Engine, com.GearBox, com.Chassis, com.DeltaTime):
            # Velocity
            velo.velV.x += accel.accV.x * dt.dt
            velo.velV.y += accel.accV.y * dt.dt

            #if abs(velo.velV.x) < 1:
            #    velo.velV.x = 0
            #print(velo.velV.y)


class PositionProcessor(esper.Processor):

    def process(self):
        for ent, (dt, velo, pos) in self.world.get_components(com.DeltaTime, com.Velocity, com.Position):
            pos.posV.x += velo.velV.x * dt.dt
            pos.posV.y += velo.velV.y * dt.dt

class RPMProcessor(esper.Processor):
    def process(self):
        for ent, (eng, grb, cha, velo, dt) in self.world.get_components(com.Engine, com.GearBox, com.Chassis, com.Velocity, com.DeltaTime):
            eng_friction_torque = (eng.rpm - eng.idle + 1)/60
            eng_torque = (eng.torque_curve[eng.rpm-eng.idle] * eng.throttle)
            if grb.gear_ratios[grb.current_gear] == 0 or grb.clutch == True:
                eng_ang_vel = eng.rpm * constants.RPM_to_RADS
                eng_ang_acc = (eng_torque - eng_friction_torque) / 0.5

                eng_ang_vel += eng_ang_acc * dt.dt
                temp_rpm = int(round(eng_ang_vel * constants.RADS_to_RPM))

                if temp_rpm < eng.idle:
                    eng.rpm = eng.idle
                elif temp_rpm > eng.rev_limit:
                    eng.rpm = eng.rev_limit
                else:
                    eng.rpm = temp_rpm
                #print(eng.rpm)
            else:
                eng.rpm = int((velo.velV.magnitude()/cha.wheel_diameter/2) * (grb.rear_diff * grb.gear_ratios[grb.current_gear]) * constants.RADS_to_RPM)

                if eng.rpm < eng.idle:
                    eng.rpm = eng.idle

                if eng.rpm >= eng.idle and eng.rpm < eng.rev_limit:
                    eng_torque = eng.torque_curve[int(eng.rpm) - eng.idle]
                else:
                    eng_torque = 0

                
                if eng.rpm < eng.idle:
                    eng.rpm = eng.idle
                elif eng.rpm > eng.rev_limit:
                    eng.rpm = eng.rev_limit

                
                cha.drive_torque = eng_torque * eng.throttle * grb.rear_diff * grb.gear_ratios[grb.current_gear]

                #eng.rpm = wheel_speed * ratio * constants.RADS_to_RPM
                #wheel_speed = (3.6 * eng.rpm * cha.wheel_diameter/2)/(grb.rear_diff * grb.gear_ratios[grb.current_gear]) * constants.RPM_to_RADS
                #print(wheel_speed)
                """
                eng_ang_vel = eng.rpm * constants.RPM_to_RADS
                eng_ang_acc = (eng_torque - eng_friction_torque ) / 0.5

                drivetrain_inertia = 0.5*ratio*ratio
                drivetrain_friction_torque = eng_friction_torque * abs(ratio)
                cha.drive_torque = eng_torque * ratio

                eng_ang_acc = (cha.drive_torque - drivetrain_friction_torque) / drivetrain_inertia
                eng_ang_vel += eng_ang_acc * dt.dt


                temp_rpm = int(round(eng_ang_vel * constants.RADS_to_RPM))
                if temp_rpm < eng.idle:
                    eng.rpm = eng.idle
                elif temp_rpm > eng.rev_limit:
                    eng.rpm = eng.rev_limit
                else:
                    eng.rpm = temp_rpm
                #print(eng.rpm)
                """

"""
class RPMProcessor(esper.Processor):

    def process(self):
        for ent, (eng, grb, dt, velo, cha) in self.world.get_components(com.Engine, com.GearBox, com.DeltaTime, com.Velocity, com.Chassis):
            if grb.clutch == False:
                # Engine inertia and we assign engine eng.rpm to a seperate variable
                eng_inertia = 0.5 * 9.34 * 0.16**2 # 0.5 * mass * radius^2
                temp_rpm = eng.rpm

                # We calculate the eng.rpm from flywheel speed and increment it by that, also check if it is within the engine limit
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
                # Get clutch eng.rpm from wheel speed
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

class SteeringProcessor(esper.Processor):

    def process(self):
        for ent, (ster, velo, cvelo, accel, caccel, cha, dt, ff, eng) in self.world.get_components(com.Steering, com.Velocity, com.CarVelocity, com.Acceleration, com.CarAcceleration, com.Chassis, com.DeltaTime, com.ForwardForce, com.Engine):
            str_ang = ster.steer_angle
            
            ster.sn = math.sin(ster.heading)
            ster.cs = math.cos(ster.heading)

            cvelo.velV.x = ster.cs*velo.velV.x + ster.sn*velo.velV.y
            cvelo.velV.y = ster.cs*velo.velV.y - ster.sn*velo.velV.x

            yawSpeedFront = cha.cg_front_axle * ster.yawRate
            yawSpeedRear = -cha.cg_rear_axle * ster.yawRate


            slipAngleFront = math.atan2(cvelo.velV.y + yawSpeedFront, abs(cvelo.velV.x)) - np.sign(cvelo.velV.x) * str_ang
            slipAngleRear  = math.atan2(cvelo.velV.y + yawSpeedRear,  abs(cvelo.velV.x))

            faw = cha.weight_front_standstill * constants.GRAVITY
            raw = cha.weight_rear_standstill * constants.GRAVITY
            
            ster.fff = np.clip(-5*slipAngleFront, -2, 2) * faw
            ster.ffr = np.clip(-5*slipAngleRear, -2, 2) * raw

            angularTorque = (ster.fff + ff.sideway_force) * cha.cg_front_axle - ster.ffr * cha.cg_rear_axle;

            if(velo.velV.magnitude() < 1 and eng.throttle == 0):
                velo.velV.y = 0
                velo.velV.x = 0
                angularTorque = 0
                yawRate = 0

            angularAccel = angularTorque / cha.inertia

            ster.yawRate += angularAccel * dt.dt
            ster.heading += ster.yawRate * dt.dt

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
            rot_spr = pygame.transform.rotate(spr.sprite, stre.heading)
            self.renderer.blit(rot_spr, [pos.posV.x, pos.posV.y])






class XXXProcessor(esper.Processor):

    def process(self):
        for ent, () in self.world.get_components():
            pass
