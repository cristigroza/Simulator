#
# (c) PySimiam Team 2014
#
# Contact person: Tim Fuchs <typograph@elec.ru>
#
# This class was implemented as a weekly programming excercise
# of the 'Control of Mobile Robots' course by Magnus Egerstedt.
#
import numpy as np
from  pose import Pose
from sensor import SonarSensor
from math import ceil, exp, sin, cos, tan, pi
from quickbot import QuickBot
import sim_server_helpers


class DRK8080_SonarSensor(SonarSensor):

     def __init__(self,pose,robot):
         # values copied from SimIAm
         x,y,fi = pose
         SonarSensor.__init__(self, pose, robot, (0.05, 2.54, fi))
         self.sensor_undetected_obstacle_color = 0x66FFC299
         self.sensor_detected_obstacle_color = 0x663300FF
         self.set_color(self.sensor_undetected_obstacle_color)




class DRK8080(QuickBot):
    """Inherts for the simobject--->robot class for behavior specific to the Khepera3""" 
    def __init__(self, pose, color = 0xFFFFFF):
        QuickBot.__init__(self, pose, color)

        self._shapes.base_plate = np.array([[ 0.0, 0.1, 1],
                                            [ 0.1, 0.0, 1],
                                            [ 0.0, -0.1, 1],
                                            [ -0.1, 0.0, 1],
                                            ])

        self.set_shape_left_wheel(np.array([[ -0.035, 0.09, 1],
                                            [ 0.035, 0.09, 1],
                                            [0.035, 0.07, 1],
                                            [-0.035, 0.07, 1]]))



        self.set_shape_right_wheel(np.array([[ -0.035, -0.09, 1],
                                            [ 0.035, -0.09, 1],
                                            [0.035, -0.07, 1],
                                            [-0.035, -0.07, 1]]))




        self.set_sonar_sensor_poses([
                            Pose(0.1*cos(np.radians(45)), 0.1*sin(np.radians(45)), np.radians(45)),
                            Pose(0.1, 0.0, np.radians(0)),
                            Pose(0.1*cos(np.radians(45)), -0.1*sin(np.radians(45)), np.radians(-45)),
                            Pose(-0.1*cos(np.radians(45)), -0.1*sin(np.radians(45)), np.radians(-135)),
                            Pose(-0.1, 0.0, np.radians(180)),

                            #The next 3 sensors are just for good looks, we don't take into account the readings
                            Pose(0.1*cos(np.radians(45)), 0.1*sin(np.radians(45)), np.radians(45)),
                            Pose(0.1, 0.0, np.radians(0)),
                            Pose(0.1*cos(np.radians(45)), -0.1*sin(np.radians(45)), np.radians(-45)),
                            Pose(-0.1*cos(np.radians(45)), -0.1*sin(np.radians(45)), np.radians(-135)),
                            Pose(-0.1, 0.0, np.radians(180)),


                          ],DRK8080_SonarSensor)
        

        self.base_plate_color = 0xB655AAEE
        # these were the original parameters
        self.info.wheels.radius = 0.035
        self.info.wheels.base_length = 0.13 # distance between the wheels
        self.info.wheels.ticks_per_rev = 4428 #????????????
        self.info.wheels.max_encoder_buffer_value = 4428
        self.info.wheels.perimeter = self.info.wheels.radius * 2 * pi

        self.info.wheels.max_velocity_ms = 0.15 #m/s
        self.info.wheels.max_velocity = 60 * self.info.wheels.max_velocity_ms / ( 2 * pi * self.info.wheels.radius) # RPM
        #self.info.wheels.min_velocity = 2*pi*30/60  #  30 RPM

        #self.info.ir_sensors.rmax = 0.8
        #self.info.ir_sensors.rmin = 0.1

        self.info.sonar_sensors.rmax = 2.54
        self.info.sonar_sensors.rmin = 0.05

    def draw(self,r):
        r.set_pose(self.get_pose())
        r.set_pen(0)

        r.set_brush(self.wheels_color)
        r.draw_polygon(self._shapes.left_wheel)
        r.draw_polygon(self._shapes.right_wheel)

        r.set_pen(0x01000000)
        r.set_brush(self.base_plate_color)
        r.draw_ellipse(0,0,0.1)



if __name__ == "__main__":
    # JP limits
    #v = max(min(v,0.314),-0.3148);
    #w = max(min(w,2.276),-2.2763);
    # Real limits
    k = DRK8080(Pose(0,0,0))
    k.set_wheel_speeds(1000,1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    k.set_wheel_speeds(1000,-1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    # 0.341 and 7.7
