
import esper
import pygame
import components as com
import constants

class BigProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff, eng, grb, cha, dt, temp) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce, com.Engine, com.GearBox, com.Chassis, com.DeltaTime, com.Temp):

            g = grb.gear_ratios[grb.current_gear]
            Radius = cha.wheel_diameter/2


            eng.rpm = (temp.v/Radius) * (grb.rear_diff * g) * constants.RADS_to_RPM

            if eng.rpm >= 0 and eng.rpm < 6800:
                eng_torque = eng.torque_curve[int(eng.rpm)]
            else:
                eng_torque = 0

            if eng.rpm < 0:
                eng.rpm = 0
            elif eng.rpm > 6799:
                eng.rpm = 6799
            else:
                eng.rpm = eng.rpm


            torque = (eng.throttle * eng_torque) * (grb.rear_diff * g)

            tractionForce = torque / Radius

            RollingResistance = 9
            AirResistance = 0.32

            dragForce = -RollingResistance * temp.v - AirResistance * temp.v * abs(temp.v);

            totalForce = dragForce + tractionForce;


            Acceleration = totalForce / cha.mass

            temp.v += Acceleration * dt.dt

            print(temp.v)

"""
            r = cha.wheel_diameter/2

            eng.rpm = int((velo.velV.y/r) * (grb.rear_diff * grb.gear_ratios[grb.current_gear]) * 30/3.14)

            if eng.rpm > 6800:
                eng.rpm = 6800
            if eng.rpm < 700:
                eng.rpm = 700
            to = eng.torque_curve[eng.rpm-eng.idle]
            cha.drive_torque = eng.throttle * to * (grb.rear_diff * grb.gear_ratios[grb.current_gear])


            ff.forward_force = (cha.drive_torque)/r
            drag_force = -(constants.DRAG_COEFF * velo.velV.magnitude() * velo.velV.y) - (constants.RR_FORCE * velo.velV.y)
            total_force = ff.forward_force + drag_force
            accel.accV.y = total_force / cha.mass
            velo.velV.y += accel.accV.y * dt.dt
            #print(velo.velV.y)
            #pos.posV.y += velo.velV.y * dt.dt
"""
class CarAccelerationProcessor(esper.Processor):

    def process(self):
        for ent, (accel, dire, velo, ff, eng, cha) in self.world.get_components(com.Acceleration, com.Direction, com.Velocity, com.ForwardForce, com.Engine, com.Chassis):
            accel.accV.x = ((dire.dirV.x * ff.forward_force) - (constants.DRAG_COEFF * velo.velV.magnitude() * velo.velV.x) - (constants.RR_FORCE * velo.velV.x)) / cha.mass
            accel.accV.y = ((dire.dirV.y * ff.forward_force) - (constants.DRAG_COEFF * velo.velV.magnitude() * velo.velV.y) - (constants.RR_FORCE * velo.velV.y)) / cha.mass


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
            ff.forward_force = (cha.drive_torque)/(cha.wheel_diameter/2)


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
                elif eng.rpm > eng.rev_limit:
                    eng.rpm = eng.rev_limit
                else:
                    eng.rpm = eng.rpm

                if eng.rpm >= eng.idle and eng.rpm < eng.rev_limit:
                    eng_torque = eng.torque_curve[int(eng.rpm) - eng.idle]
                else:
                    eng_torque = 0
                

                
                cha.drive_torque = eng_torque * eng.throttle * grb.rear_diff * grb.gear_ratios[grb.current_gear]

                #eng.rpm = wheel_speed * ratio * constants.RADS_to_RPM
                wheel_speed = (3.6 * eng.rpm * cha.wheel_diameter/2)/(grb.rear_diff * grb.gear_ratios[grb.current_gear]) * constants.RPM_to_RADS
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
