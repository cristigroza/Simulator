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
from sensor import  SonarSensor, IRSensor
from math import ceil, exp, sin, cos, tan, pi,radians
from quickbot import QuickBot
import sim_server_helpers

class i90_IRSensor(IRSensor):
    """Inherits from the proximity sensor class. Performs calculations specific to the khepera3 for its characterized proximity sensors"""

    def __init__(self,pose,robot):
        # values copied from SimIAm
        IRSensor.__init__(self, pose, robot, (0.1, 0.8, np.radians(6)))


class i90_SonarSensor(SonarSensor):

     def __init__(self,pose,robot):
         # values copied from SimIAm
         x,y,fi = pose
         SonarSensor.__init__(self, pose, robot, (0.05, 2.54,fi))
         self.sensor_undetected_obstacle_color = 0x66FFC299
         self.sensor_detected_obstacle_color = 0x663300FF
         self.set_color(self.sensor_undetected_obstacle_color)


class i90(QuickBot):
    """Inherts for the simobject--->robot class for behavior specific to the Khepera3""" 
    def __init__(self, pose, color = 0xFFFFFF):
        QuickBot.__init__(self, pose, color)

        self.set_shape_base_plate(np.array([
                                            [ -0.215, 0.12842, 1],
                                            [ -0.078, 0.19, 1],
                                            [ -0.0316, 0.19, 1],
                                            [ -0.0316, 0.12857, 1],
                                            [ 0.1493, 0.12857, 1],
                                            [ 0.1493, 0.19, 1],
                                            [ 0.1613, 0.19, 1],
                                            [ 0.1923, 0.1599, 1],
                                            [ 0.215, 0.1081, 1],
                                            [ 0.215, -0.1081, 1],
                                            [ 0.1923, -0.1599, 1],
                                            [ 0.1613, -0.19, 1],
                                            [ 0.1493, -0.19, 1],
                                            [ 0.1493, -0.12857, 1],
                                            [ -0.0316, -0.12857, 1],
                                            [ -0.0316, -0.19, 1],
                                            [ -0.078, -0.19, 1],
                                            [ -0.215, -0.12842, 1],

                                            ]))

        self.set_shape_upper_plate_front(np.array([
                                            [ 0.1309, 0.0985, 1],
                                            [ 0.1923, 0.1599, 1],
                                            [ 0.215, 0.1081, 1],
                                            [ 0.215, -0.1081, 1],
                                            [ 0.1923, -0.1599, 1],
                                            [ 0.1309, -0.0985, 1],

                                            ]))
        self.set_shape_upper_plate(np.array([
                                           [ 0.1309, 0.0985, 1],
                                            [ 0.1309, -0.0985, 1],
                                            [ -0.0965, -0.0985, 1],
                                            [ -0.0965, 0.0985, 1]
                                            ]))

        self.set_shape_upper_plate_back(np.array([

                                            [ -0.0965, 0.0985, 1],
                                            [ -0.0965, -0.0985, 1],
                                            [ -0.215, -0.12842, 1],
                                            [ -0.215, 0.12842, 1],
                                            ]))


        self.set_shape_left_wheel(np.array([[-0.0216, 0.18, 1],
                                            [ 0.1393, 0.18, 1],
                                            [ 0.1393, 0.11857, 1],
                                            [-0.0216, 0.11857, 1]]))


        self.set_shape_right_wheel(np.array([[-0.0216, -0.18, 1],
                                            [ 0.1393, -0.18, 1],
                                            [ 0.1393, -0.11857, 1],
                                            [-0.0216, -0.11857, 1]]))


        self.set_ir_sensor_poses([
                          Pose( 0.1493, 0.19, np.radians(90)),
                          Pose( 0.1843, 0.1729, np.radians(45)),
                          Pose( 0.2083, 0.1359, np.radians(20)),
                          Pose( 0.215, 0.08658, np.radians(0)),
                          Pose( 0.215, 0.0, np.radians(0)),
                          Pose( 0.215, -0.08658, np.radians(0)),
                          Pose( 0.2083 , -0.1359, np.radians(-20)),
                          Pose( 0.1843, -0.1729, np.radians(-45)),
                          Pose( 0.1493, -0.19, np.radians(-90))
                          ],i90_IRSensor)

        self.set_sonar_sensor_poses([
                          Pose( 0.2083, 0.1359, np.radians(20)),
                          Pose( 0.215, 0.0, np.radians(0)),
                          Pose( 0.2083 , -0.1359, np.radians(-20)),

                          #The next 3 sensors are just for good looks, we don't take into account the readings
                          Pose( 0.2083, 0.1359, np.radians(20)),
                          Pose( 0.215, 0.0, np.radians(0)),
                          Pose( 0.2083 , -0.1359, np.radians(-20)),
                          ],i90_SonarSensor)


        self.base_plate_color = 0xB6FF6600

        self.upper_plate_color = 0xF6C0C0C0
        self.upper_plate_front_color = 0xB6808080
        self.upper_plate_back_color = 0xB6808080
        # these were the original parameters
        self.info.wheels.radius = 0.0825
        self.info.wheels.base_length = 0.32 # distance between the wheels
        self.info.wheels.ticks_per_rev = 800
        self.info.wheels.max_encoder_buffer_value = 32767
        self.info.wheels.perimeter = self.info.wheels.radius * 2 * pi

        self.info.wheels.max_velocity_ms = 0.75 #m/s
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
    k = i90(Pose(0,0,0))
    k.set_wheel_speeds(1000,1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    k.set_wheel_speeds(1000,-1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    # 0.341 and 7.7
