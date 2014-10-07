#
# (c) PySimiam Team 2014
#
# Contact person: Tim Fuchs <typograph@elec.ru>
#
# This class was implemented as a weekly programming excercise
# of the 'Control of Mobile Robots' course by Magnus Egerstedt.
#
import numpy as np
from pose import Pose
from sensor import SonarSensor, IRSensor
from math import ceil, exp, sin, cos, tan, pi, radians
from quickbot import QuickBot
import sim_server_helpers

class x80H_IRSensor(IRSensor):
    """Inherits from the proximity sensor class. Performs calculations specific to the khepera3 for its characterized proximity sensors"""

    def __init__(self,pose,robot):
        # values copied from SimIAm
        IRSensor.__init__(self, pose, robot, (0.1, 0.8, np.radians(6)))


class x80H_SonarSensor(SonarSensor):

     def __init__(self,pose,robot):
         # values copied from SimIAm
         x,y,fi = pose
         SonarSensor.__init__(self, pose, robot, (0.05, 2.54, fi))
         self.sensor_undetected_obstacle_color = 0x6680CC99
         self.sensor_detected_obstacle_color = 0x663300FF
         self.set_color(self.sensor_undetected_obstacle_color)


class x80H(QuickBot):
    """Inherts for the simobject--->robot class for behavior specific to the Khepera3""" 
    def __init__(self, pose, color = 0xFFFFFF):
        QuickBot.__init__(self, pose, color)

        self.set_shape_base_plate(np.array([[ -0.085, 0.2, 1],
                                            [ 0.085, 0.2, 1],

                                            [ 0.075 + 0.115*cos(radians(80)), 0.003+ 0.2*sin(radians(80)), 1],
                                            [ 0.065 + 0.115*cos(radians(70)), 0.009 + 0.2*sin(radians(70)), 1],
                                            [ 0.060 + 0.115*cos(radians(60)), 0.015+0.2*sin(radians(60)), 1],
                                            [ 0.085 + 0.115*cos(radians(50)), 0.2*sin(radians(50)), 1],
                                            [ 0.085 + 0.115*cos(radians(40)), 0.2*sin(radians(40)), 1],
                                            [ 0.085 + 0.115*cos(radians(30)), 0.2*sin(radians(30)), 1],
                                            [ 0.085 + 0.115*cos(radians(20)), 0.2*sin(radians(20)), 1],
                                            [ 0.085 + 0.115*cos(radians(10)), 0.2*sin(radians(10)), 1],

                                            [ 0.2, 0.0000, 1],

                                            [ 0.085 + 0.115*cos(radians(10)), -0.2*sin(radians(10)), 1],
                                            [ 0.085 + 0.115*cos(radians(20)), -0.2*sin(radians(20)), 1],
                                            [ 0.085 + 0.115*cos(radians(30)), -0.2*sin(radians(30)), 1],
                                            [ 0.085 + 0.115*cos(radians(40)), -0.2*sin(radians(40)), 1],
                                            [ 0.085 + 0.115*cos(radians(50)), -0.2*sin(radians(50)), 1],
                                            [ 0.060 + 0.115*cos(radians(60)), -0.015 - 0.2*sin(radians(60)), 1],
                                            [ 0.065 + 0.115*cos(radians(70)), -0.009 - 0.2*sin(radians(70)), 1],
                                            [ 0.075 + 0.115*cos(radians(80)), -0.003 - 0.2*sin(radians(80)), 1],

                                            [ 0.085,-0.2, 1],
                                            [ -0.085,-0.2, 1],

                                            [-0.2,-0.061, 1],
                                            [-0.2, 0.061, 1],

                                            ]))

        self.set_shape_upper_plate(np.array([
                                            [ 0.02, 0.15, 1],
                                            [ 0.085, 0.15, 1],
                                            [ 0.085, 0.2, 1],

                                            [ 0.075 + 0.115*cos(radians(80)), 0.003+ 0.2*sin(radians(80)), 1],
                                            [ 0.065 + 0.115*cos(radians(70)), 0.009 + 0.2*sin(radians(70)), 1],
                                            [ 0.060 + 0.115*cos(radians(60)), 0.015+0.2*sin(radians(60)), 1],
                                            [ 0.085 + 0.115*cos(radians(50)), 0.2*sin(radians(50)), 1],
                                            [ 0.085 + 0.115*cos(radians(40)), 0.2*sin(radians(40)), 1],
                                            [ 0.085 + 0.115*cos(radians(30)), 0.2*sin(radians(30)), 1],
                                            [ 0.085 + 0.115*cos(radians(20)), 0.2*sin(radians(20)), 1],
                                            [ 0.085 + 0.115*cos(radians(10)), 0.2*sin(radians(10)), 1],

                                            [ 0.2, 0.0000, 1],

                                            [ 0.085 + 0.115*cos(radians(10)), -0.2*sin(radians(10)), 1],
                                            [ 0.085 + 0.115*cos(radians(20)), -0.2*sin(radians(20)), 1],
                                            [ 0.085 + 0.115*cos(radians(30)), -0.2*sin(radians(30)), 1],
                                            [ 0.085 + 0.115*cos(radians(40)), -0.2*sin(radians(40)), 1],
                                            [ 0.085 + 0.115*cos(radians(50)), -0.2*sin(radians(50)), 1],
                                            [ 0.060 + 0.115*cos(radians(60)), -0.015 - 0.2*sin(radians(60)), 1],
                                            [ 0.065 + 0.115*cos(radians(70)), -0.009 - 0.2*sin(radians(70)), 1],
                                            [ 0.075 + 0.115*cos(radians(80)), -0.003 - 0.2*sin(radians(80)), 1],

                                            [ 0.085,-0.2, 1],
                                            [ 0.085,-0.15, 1],
                                            [ 0.02,-0.15, 1],
                                            ]))



        self.set_shape_left_wheel(np.array([[ 0.083, 0.19, 1],
                                            [ 0.083, 0.154, 1],
                                            [-0.081, 0.154, 1],
                                            [-0.081, 0.19, 1]]))


        self.set_shape_right_wheel(np.array([[ 0.083, -0.19, 1],
                                            [ 0.083, -0.154, 1],
                                            [-0.081, -0.154, 1],
                                            [-0.081, -0.19, 1]]))


        self.set_ir_sensor_poses([
                          Pose( 0.085 + 0.115*cos(radians(30)), 0.2*sin(radians(30)), np.radians(30)),
                          #Pose( 0.085 + 0.115*cos(radians(12)), 0.2*sin(radians(12)), np.radians(12)),
                          Pose( -0.2, 0.0, np.radians(180)),
                          Pose( 0.085 + 0.115*cos(radians(12)), -0.2*sin(radians(12)), np.radians(-12)),
                          Pose(0.085 + 0.115*cos(radians(30)), -0.2*sin(radians(30)), np.radians(-30)),
                          Pose( 0,-0.2, np.radians(-90)),
                          Pose( 0, 0.2, np.radians(90)),
                          ],x80H_IRSensor)

        self.set_sonar_sensor_poses([
                          Pose(0.085 + 0.115*cos(radians(45)), 0.2*sin(radians(45)), np.radians(45)),
                          Pose( 0.2, 0.0, np.radians(0)),
                          Pose(0.085 + 0.115*cos(radians(45)), -0.2*sin(radians(45)), np.radians(-45)),

                          #The next 3 sensors are just for good looks, we don't take into account the readings
                          Pose(0.085 + 0.115*cos(radians(45)), 0.2*sin(radians(45)), np.radians(45)),
                          Pose( 0.2, 0.0, np.radians(0)),
                          Pose(0.085 + 0.115*cos(radians(45)), -0.2*sin(radians(45)), np.radians(-45)),

                          ],x80H_SonarSensor)


        self.base_plate_color = 0x66A5A5A5
        self.upper_plate_color = 0xF6A5A5A5
        # these were the original parameters
        self.info.wheels.radius = 0.0825
        self.info.wheels.base_length = 0.26 # distance between the wheels
        self.info.wheels.ticks_per_rev = 1200
        self.info.wheels.max_encoder_buffer_value = 32767
        self.info.wheels.perimeter = self.info.wheels.radius * 2 * pi

        self.info.wheels.max_velocity_ms = 1 #m/s
        self.info.wheels.max_velocity = 60 * self.info.wheels.max_velocity_ms / ( 2 * pi * self.info.wheels.radius) #RPM
        #self.info.wheels.min_velocity = 2*pi*30/60  #  30 RPM

        self.info.ir_sensors.rmax = 0.8
        self.info.ir_sensors.rmin = 0.1

        self.info.sonar_sensors.rmax = 2.54
        self.info.sonar_sensors.rmin = 0.05


if __name__ == "__main__":
    # JP limits
    #v = max(min(v,0.314),-0.3148);
    #w = max(min(w,2.276),-2.2763);
    # Real limits
    k = x80H(Pose(0,0,0))
    k.set_wheel_speeds(1000,1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    k.set_wheel_speeds(1000,-1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    # 0.341 and 7.7
