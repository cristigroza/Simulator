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
from sensor import ProximitySensor
from robot import Robot
from math import ceil, exp, sin, cos, tan, pi
from helpers import Struct
import sim_server_helpers

class QuickBot_IRSensor(ProximitySensor):
    """Inherits from the proximity sensor class. Performs calculations specific to the khepera3 for its characterized proximity sensors"""
    
    ir_coeff = sim_server_helpers.compute_x80_ir_coeff()
    
    def __init__(self,pose,robot):
        # values copied from SimIAm    
        ProximitySensor.__init__(self, pose, robot, (0.1, 0.8, np.radians(6)))

    def distance_to_value(self,dst):
        """Returns the distance calculation from the distance readings of the proximity sensors""" 

        if dst < self.rmin :
            return 3446
        elif dst > self.rmax:
            return 585
        else:
            return np.polyval(self.ir_coeff,dst)

class QuickBot_SonarSensor(ProximitySensor):

     def __init__(self,pose,robot):
         # values copied from SimIAm
         ProximitySensor.__init__(self, pose, robot, (0.05, 2.54, np.radians(8)))
         self.sensor_undetected_obstacle_color = 0x66BFEFFF
         self.sensor_detected_obstacle_color = 0x663300FF
         self.set_color(self.sensor_undetected_obstacle_color)

     def distance_to_value(self,dst):
        """Returns the distance calculation from the distance readings of the proximity sensors"""

        if dst < self.rmin :
            return 0.04
        elif dst > self.rmax:
            return 2.54
        else:
            return dst


class QuickBot(Robot):

    def _set_default_settings(self):
                # default shape
        self._shapes.base_plate = np.array([[ 0.0335, 0.0534, 1],
                                            [ 0.0429, 0.0534, 1],
                                            [ 0.0639, 0.0334, 1],
                                            [ 0.0686, 0.0000, 1],
                                            [ 0.0639,-0.0334, 1],
                                            [ 0.0429,-0.0534, 1],
                                            [ 0.0335,-0.0534, 1],
                                            [-0.0584,-0.0534, 1],
                                            [-0.0912,-0.0297, 1],
                                            [-0.1012,-0.0227, 1],
                                            [-0.1012, 0.0227, 1],
                                            [-0.0912, 0.0297, 1],
                                            [-0.0584, 0.0534, 1],
                                            ])
        self._shapes.upper_plate = None
        self._shapes.upper_plate_front = None
        self._shapes.upper_plate_back = None
        self._shapes.head = None
        self._shapes.left_wheel = np.array([[ 0.0204, 0.0595, 1],
                                            [ 0.0204, 0.045, 1],
                                            [-0.0484, 0.045, 1],
                                            [-0.0484, 0.0595, 1]])

        self._shapes.left_wheel_ol = np.array([[ 0.0254, 0.0595, 1],
                                               [ 0.0254, 0.0335, 1],
                                               [-0.0384, 0.0335, 1],
                                               [-0.0384, 0.0595, 1]])

        self._shapes.right_wheel_ol = np.array([[ 0.0254,-0.0595, 1],
                                                [ 0.0254,-0.0335, 1],
                                                [-0.0384,-0.0335, 1],
                                                [-0.0384,-0.0595, 1]])

        self._shapes.right_wheel = np.array([[ 0.0204,-0.0595, 1],
                                             [ 0.0204,-0.045, 1],
                                             [-0.0484,-0.045, 1],
                                             [-0.0484,-0.0595, 1]])




        ir_sensor_poses = []
        sonar_sensor_poses = []

        # these were the original parameters
        self.info.wheels.radius = 0.085
        self.info.wheels.base_length = 0.3 # distance between the wheels
        self.info.wheels.ticks_per_rev = 1200
        self.info.wheels.max_encoder_buffer_value = 32000

        self.info.wheels.left_ticks = 0
        self.info.wheels.right_ticks = 0

        self.info.wheels.perimeter = self.info.wheels.radius * 2 * pi


        self.info.wheels.max_velocity = 2*pi*130/60 # 130 RPM
        self.info.wheels.min_velocity = 2*pi*30/60  #  30 RPM

        self.left_revolutions = 0.0
        self.right_revolutions = 0.0

        self.info.ir_sensors = Struct()
        self.info.ir_sensors.poses = ir_sensor_poses
        self.info.ir_sensors.readings = None
        self.info.ir_sensors.rmax = 0.8
        self.info.ir_sensors.rmin = 0.1

        self.info.sonar_sensors = Struct()
        self.info.sonar_sensors.poses = sonar_sensor_poses
        self.info.sonar_sensors.readings = None
        self.info.sonar_sensors.rmax = 2.54
        self.info.sonar_sensors.rmin = 0.05

        self.wheels_color = 0x000000
        self.base_plate_color = 0x55AAEE
        self.upper_plate_color = None
        self.upper_plate_front_color = None
        self.upper_plate_back_color = None
        self.head_color = None

    """Inherts for the simobject--->robot class for behavior specific to the Khepera3""" 
    def __init__(self, pose, color = 0xFFFFFF):
        Robot.__init__(self, pose, color)
        
        # create shape
        self._shapes = Struct()
        # create IR sensors
        self.ir_sensors = []
        # create Sonar sensors
        self.sonar_sensors = []
        # initialize motion
        self.ang_velocity = (0.0,0.0)

        self.info = Struct()
        self.info.wheels = Struct()
        self.colors = {}
        self._set_default_settings()

    #Set robot ir_sensor_poses
    def set_ir_sensor_poses(self, ir_sensor_poses,IrClass):
        self.info.ir_sensors.poses = ir_sensor_poses
        self.ir_sensors = []
        for pose in ir_sensor_poses:
            self.ir_sensors.append(IrClass(pose,self))

    #Set robot sonar_sensors
    def set_sonar_sensor_poses(self, sonar_sensor_poses,SonarClass):
        self.info.sonar_sensors.poses = sonar_sensor_poses
        self.sonar_sensors = []
        for pose in sonar_sensor_poses:
            self.sonar_sensors.append(SonarClass(pose,self))

    #Set robot shape
    def set_shape_head(self,head):
        self._shapes.head = head

    def set_shape_upper_plate(self,upper_plate):
        self._shapes.upper_plate = upper_plate

    def set_shape_upper_plate_front(self,upper_plate_front):
        self._shapes.upper_plate_front = upper_plate_front

    def set_shape_upper_plate_back(self,upper_plate_back):
        self._shapes.upper_plate_back = upper_plate_back

    def set_shape_base_plate(self,base_plate):
        self._shapes.base_plate = base_plate

    def set_shape_left_wheel(self,left_wheel):
        self._shapes.left_wheel = left_wheel

    def set_shape_right_wheel(self,right_wheel):
        self._shapes.right_wheel = right_wheel

    def set_shape_left_wheel_ol(self,left_wheel_ol):
        self._shapes.left_wheel_ol = left_wheel_ol

    def set_shape_right_wheel_ol(self,right_wheel_ol):
        self._shapes.right_wheel_ol = right_wheel_ol

    def draw(self,r):
        r.set_pose(self.get_pose())
        r.set_pen(0)

        r.set_brush(self.wheels_color)
        r.draw_polygon(self._shapes.left_wheel)
        r.draw_polygon(self._shapes.right_wheel)
        
        r.set_pen(0x01000000)
        r.set_brush(self.base_plate_color)
        r.draw_polygon(self._shapes.base_plate)

        if self._shapes.upper_plate != None:
            r.set_pen(0x01000000)
            r.set_brush(self.upper_plate_color)
            r.draw_polygon(self._shapes.upper_plate)
        if self._shapes.upper_plate_front != None:
                r.set_pen(0x01000000)
                r.set_brush(self.upper_plate_front_color)
                r.draw_polygon(self._shapes.upper_plate_front)
        if self._shapes.upper_plate_back != None:
                r.set_pen(0x01000000)
                r.set_brush(self.upper_plate_back_color)
                r.draw_polygon(self._shapes.upper_plate_back)

        if self._shapes.head != None:
            r.set_pen(0x01000000)
            r.set_brush(self.head_color)
            r.draw_polygon(self._shapes.head)

        r.set_pen(0x10000000)
        r.set_brush(None)
        r.draw_polygon(self._shapes.left_wheel)
        r.draw_polygon(self._shapes.right_wheel)        

        
    def get_envelope(self):
        return self._shapes.base_plate
    
    def move(self,dt):
        # There's no need to use the integrator - these equations have a solution        
        (vl, vr) = self.get_wheel_speeds()
        (v,w) = self.diff2uni((vl,vr))
        x, y, theta = self.get_pose()
        if w == 0:
            x += v*cos(theta)*dt
            y += v*sin(theta)*dt
        else:
            dtheta = w*dt
            x += 2*v/w*cos(theta + dtheta/2)*sin(dtheta/2)
            y += 2*v/w*sin(theta + dtheta/2)*sin(dtheta/2)
            theta += dtheta
        
        self.set_pose(Pose(x, y, (theta + pi)%(2*pi) - pi))

        self.left_revolutions += vl*dt/2/pi
        self.right_revolutions += vr*dt/2/pi
        #self.info.wheels.left_ticks = int(self.left_revolutions*self.info.wheels.ticks_per_rev)
        #self.info.wheels.right_ticks = int(self.right_revolutions*self.info.wheels.ticks_per_rev)
        
    def get_info(self):
        self.info.ir_sensors.readings = [sensor.reading() for sensor in self.ir_sensors]
        self.info.sonar_sensors.readings = [sensor.reading() for sensor in self.sonar_sensors]
        return self.info
    
    def set_inputs(self,inputs):
        self.set_wheel_speeds(inputs)
    
    def diff2uni(self,diff):
        (vl,vr) = diff
        v = (vl+vr) * self.info.wheels.radius/2;
        w = (vr-vl) * self.info.wheels.radius/self.info.wheels.base_length;
        return (v,w)
    
    def get_wheel_speeds(self):
        return self.ang_velocity
    
    def set_wheel_speeds(self,*args):
        if len(args) == 2:
            (vl, vr) = args
        else:
            (vl, vr) = args[0]
            
        left_ms  = max(-self.info.wheels.max_velocity, min(self.info.wheels.max_velocity, vl))
        right_ms = max(-self.info.wheels.max_velocity, min(self.info.wheels.max_velocity, vr))

        self.ang_velocity = (left_ms, right_ms)

    def get_external_sensors(self):
        return self.ir_sensors

    def get_sonar_sensors(self):
        return self.sonar_sensors

    def draw_ir_sensors(self,renderer):
        """Draw the sensors that this robot has"""
        for sensor in self.ir_sensors:
            sensor.draw(renderer)


    def draw_all_sonar_sensors(self,renderer):
        for sensor in self.sonar_sensors:
            sensor.draw(renderer)

    def draw_half_sonar_sensors(self,renderer):
        for sensor in self.sonar_sensors[:len(self.sonar_sensors)/2]:
            sensor.draw(renderer)

    def update_sensors(self):
        for sensor in self.ir_sensors:
            sensor.update_distance()
        for sensor in self.sonar_sensors:
            sensor.update_distance()
    
if __name__ == "__main__":
    # JP limits
    #v = max(min(v,0.314),-0.3148);
    #w = max(min(w,2.276),-2.2763);
    # Real limits
    k = QuickBot(Pose(0,0,0))
    k.set_wheel_speeds(1000,1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    k.set_wheel_speeds(1000,-1000)
    print(k.diff2uni(k.get_wheel_speeds()))
    # 0.341 and 7.7
