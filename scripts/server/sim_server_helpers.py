import math
import numpy as np
def buildTuple(command):

    list = command.split(';')
    args = [ int(x) for x in list[1:] ] if command.count(';') > 1 else None
    tpl = (list[0],args)
    return tpl

def computeRotation(max_encoder_buffer_value, new_value, old_value):
    a1 = new_value - old_value
    direction = math.copysign(1.,a1)
    a1=abs(a1)
    a2 = abs(max_encoder_buffer_value - abs(a1))

    direction  = direction if min(a1,a2) == a1 else -direction
    val = direction * min( a1, a2 )
    return val


def computeWheelRotationSpeed(robot, new_value, old_value, run_time):
    rotation = computeRotation(robot.info.wheels.max_encoder_buffer_value, new_value, old_value)
    v = (robot.info.wheels.perimeter * rotation)/(run_time * robot.info.wheels.ticks_per_rev)
    return v

def compute_ir_coeff():

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
