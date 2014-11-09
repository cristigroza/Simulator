#
# Sensors
#
# In the original Sim.I.Am code there is no base class, as the sensors are
# completely arbitrary objects
#

import random
import numpy as np
from simobject import SimObject
from pose import Pose
from math import sin, cos, sqrt, radians,pi
import global_val
from robot import Robot

class Sensor:
    """Base superclass for sensor objects"""
    @classmethod
    def add_gauss_noise(value, sigma):
        """Returns the value with an added normal noise
        
        The return value is normally distributed around value with a standard deviation sigma
        """
        return random.gauss(value,sigma)
  
class MountedSensor(SimObject, Sensor):
    """A sensor that moves together with its parent object.
    
       The sensor is assumed to be attached to *parent* at *pose* in local
       coordinates.
    """
    def __init__(self,pose,parent):
        SimObject.__init__(self,pose)
        self.__frame = parent

    def get_internal_pose(self):
        """Get the pose of the sensor in the parent (robot) coordinates."""
        return SimObject.get_pose(self)
       
    def get_pose(self):
        x, y, t = SimObject.get_pose(self)
        rx, ry, rt = self.__frame.get_pose()
        return Pose(rx+x*cos(rt)-y*sin(rt),ry+x*sin(rt)+y*cos(rt),t+rt)
    
class ProximitySensor(MountedSensor):
    """Create a proximity sensor mounted on robot at *pose*. The geometry
       is a (rmin, rmax, angle) tuple.
    """
    def __init__(self,pose,robot,geometry):
        """Create a proximity sensor mounted on robot at pose. The geometry
        is a (rmin, rmax, angle) tuple
        """
        MountedSensor.__init__(self,pose,robot)
        self.rmin, self.rmax, self.phi = geometry
        self.pts = self.get_cone(self.rmax)
        self.fullcone = [(0,0),
                         (self.rmax*cos(self.phi/2),self.rmax*sin(self.phi/2)),
                         (self.rmax,0),
                         (self.rmax*cos(self.phi/2),-self.rmax*sin(self.phi/2))]
                    
        self.__distance = 65536
        self.sensor_detected_obstacle_color = 0xCCFF5566
        self.sensor_undetected_obstacle_color = 0x33FF5566
        self.set_color(self.sensor_undetected_obstacle_color)

    def add_gauss_noise(self,value, sigma):
        """Returns the value with an added normal noise

        The return value is normally distributed around value with a standard deviation sigma
        """
        return random.gauss(value,sigma)
    def get_cone(self, distance):
        return [(self.rmin*cos(self.phi/2),self.rmin*sin(self.phi/2)),
                (distance*cos(self.phi/2),distance*sin(self.phi/2)),
                (distance,0),
                (distance*cos(self.phi/2),-distance*sin(self.phi/2)),
                (self.rmin*cos(self.phi/2),-self.rmin*sin(self.phi/2))]
        
    def get_envelope(self):
        """Return the envelope of the sensor"""
        return self.fullcone

    def distance_to_value(self,dst):
        """Returns the distance to the value using sensor calculations"""
        raise NotImplementedError("ProximitySensor.distance_to_value")
        
    def distance(self):
        """Returns the distance instance"""
        return self.__distance
    
    def reading(self):
        """Returns the reading value"""
        return self.distance_to_value(self.distance())

    def update_distance(self, sim_object = None):
        """updates all the distances from the reading"""
        if sim_object is None:
            # reset distance to max
            self.__distance = 65536
            self.set_color(self.sensor_undetected_obstacle_color)
            self.pts = self.get_cone(self.rmax)
            return True
        else:
            distance_to_obj = self.get_distance_to(sim_object)
            if distance_to_obj:
                if self.__distance > distance_to_obj:
                    #self.set_color(0x336655FF)
                    self.set_color(self.sensor_detected_obstacle_color)
                    self.pts = self.get_cone(distance_to_obj)
                    self.__distance = distance_to_obj
                    return True
        return False

    def draw(self, r):
        """draws the sensor simobject"""
        r.set_pose(self.get_pose())
        r.set_brush(self.get_color())
        r.draw_ellipse(0,0,min(1,self.rmin/5),min(1,self.rmin/5))

        r.draw_polygon(self.pts)
        
    def get_distance_to(self, sim_object):
        """Gets the distance to another simobject
        returns distance in meters or None if not in contact"""
        ox, oy, ot = self.get_pose()
        min_distance = None
        for px, py in self.get_contact_points(sim_object):
            distance = sqrt((px-ox)*(px-ox)+(py-oy)*(py-oy))
            if min_distance is not None:
                if distance < min_distance:
                    min_distance = distance
            else: min_distance = distance
        return min_distance

class SonarSensor(ProximitySensor):

     def __init__(self,pose,robot,geometry):
        """Create a proximity sensor mounted on robot at pose. The geometry
        is a (rmin, rmax, angle) tuple
        """
        ProximitySensor.__init__(self,pose,robot,geometry)
        self.rmin, self.rmax, self.phi = geometry
        self.fullcone = self.get_cone(self.rmax)

     def get_cone(self, distance):

        fi_m = [ pi/4+(x*1.0)/10 for x in range(0,9)]
        x1 = [(distance * cos(fi)) * fi *1.8 * cos(fi) for fi in fi_m]
        y1 = [(distance * cos(fi)) * fi *1.8 * sin(fi) for fi in fi_m]
        xr = [ x * cos(-pi/4) - y *sin(-pi/4) for x,y in zip(x1,y1)]
        yr = [ x * sin(-pi/4) + y *cos(-pi/4) for x,y in zip(x1,y1)]
        yr_n = [-y for y in yr]
        upper_half = zip(xr,yr)
        lower_half = zip(xr,yr_n)
        rev_lower_half = lower_half[::-1]
        return upper_half + rev_lower_half

     def get_envelope(self):
        """Return the envelope of the sensor"""
        return self.fullcone
     def get_distance_to(self, sim_object):
        """Gets the distance to another simobject
        returns distance in meters or None if not in contact"""
        ox, oy, ot = self.get_pose()
        min_distance = None
        for px, py in self.get_contact_points(sim_object):
            distance = sqrt((px-ox)*(px-ox)+(py-oy)*(py-oy))
            if min_distance is not None:
                if distance < min_distance:
                    min_distance = distance
            else: min_distance = distance
        return min_distance

     def _limit_dst(self,dst):
        if dst > 254:
            return 254
        elif dst < 4:
            return 4
        else:
            return dst

     def distance_to_value(self,dst_in_m):
        """Returns the distance calculation from the distance readings of the proximity sensors"""

        if dst_in_m < self.rmin :
            return 4
        elif dst_in_m > self.rmax:
            return 254
        else:
             dst_in_cm = self.add_gauss_noise(dst_in_m * 100, global_val.sonar_sigma_deviation)
             return self._limit_dst(dst_in_cm)


class IRSensor(ProximitySensor):
    """Inherits from the proximity sensor class. Performs calculations specific to the khepera3 for its characterized proximity sensors"""

    def __init__(self,pose,robot, geometry):
        # values copied from SimIAm

        ProximitySensor.__init__(self, pose, robot, geometry)
        self.ir_coeff = self.compute_ir_coeff()

    def _distance2ival(self, dst):
        value = np.polyval(self.ir_coeff,dst)
        valueWithNoise = self.add_gauss_noise(value,global_val.ir_sigma_deviation)
        return valueWithNoise

    def _limit_ival(self, ival):
        if ival > 3446:
            return 3446
        elif ival < 585:
            return 585
        else:
            return ival

    def distance_to_value(self,dst):
        """Returns the distance calculation from the distance readings of the proximity sensors"""

        if dst < self.rmin :
            return 3446
        elif dst > self.rmax:
            return 585
        else:
            ival = self._distance2ival(dst)
            return self._limit_ival(ival)

    def compute_ir_coeff(self):

        x = np.array([x*1.0/100 for x in range(8,81) if x%2==0])#Distance
        y = np.array([2.752, 2.3,    2.275, 1.8,
                      1.589, 1.445,  1.3,   1.22,
                      1.121, 1.075,  0.95,  0.9314,
                      0.9,   0.8725, 0.825, 0.78,
                      0.735, 0.714,  0.69,  0.667,
                      0.625, 0.6,    0.59,  0.584,
                      0.565, 0.525,  0.511, 0.5,
                      0.497, 0.48,   0.45,  0.44,
                      0.43,  0.42,   0.41,  0.405,
                      0.4]) #Analog voltage output
        coeff = np.array([x*4095/3 for x in np.polyfit(x, y, 3)])
        return coeff
