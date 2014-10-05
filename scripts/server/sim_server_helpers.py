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

def compute_x80_ir_coeff():

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
def convertPWMToVelocity(robot, pwm_command):
    stop_value = 16384
    min_pwm = 8000
    max_pwm = 32767
    max_rpm = robot.info.wheels.max_velocity
    if pwm_command == stop_value:
        return 0

    if pwm_command < min_pwm or (pwm_command - stop_value < min_pwm and pwm_command - stop_value > 0 ):
        return 0

    sign = math.copysign(1.,pwm_command - stop_value)

    coeff = gen_poly_coeff_v1(max_pwm,min_pwm, max_rpm)

    if pwm_command < stop_value:
        v = pwm2pwm(pwm_command, coeff) / max_rpm
    else:
        pwm_command -= stop_value
        v = pwm2pwm(pwm_command, coeff) / max_rpm

    return sign * v
def pwm2pwm(pwm_command, coeff):
    return  np.polyval(coeff,pwm_command)

#A bit not stable
def gen_poly_coeff_v1(max_pwm,min_pwm, max_rpm):
    # x * 32767 / 280 = val_c (x [70, 80, 90, ... 280])
    pwm = np.array([min_pwm] + [x * max_pwm / 28 for x in range(7,29)])
    rpm = np.array( [x * max_rpm / 180 for x in [0, 33, 105, 130, 141, 148, 154, 158, 162, 167, 168, 169, 170, 172, 173, 174, 175, 176, 177, 178, 179, 179.5, 180 ]]) #Analog voltage output
    coeff = np.array([x for x in np.polyfit(pwm, rpm, 9)])
    return coeff
#Stable
def gen_poly_coeff_v2(max_pwm,min_pwm, max_rpm):
    # x * 32767 / 280 = val_c (x [70, 80, 90, ... 280])
    pwm = np.array([min_pwm] + [x * max_pwm / 28 for x in range(7,29)])
    rpm = np.array( [x * max_rpm / 180 for x in [0, 18, 57, 80, 98, 113, 125, 135, 143, 149, 154, 158, 162, 166, 169, 171, 173, 174, 175, 177, 178, 179, 180]]) #Analog voltage output
    coeff = np.array([x for x in np.polyfit(pwm, rpm, 6)])
    return coeff

def convertVelocityToRobotTicks(velocity, time, current_pos, robot_info):
    max_encoder_value = robot_info.wheels.max_encoder_buffer_value
    ticks_per_rev = robot_info.wheels.ticks_per_rev
    perimeter = robot_info.wheels.perimeter
    distance = velocity * time
    ticks = distance * ticks_per_rev / perimeter
    ticks = math.copysign(1.,ticks) * math.fabs(ticks) % max_encoder_value
    current_pos += ticks

    if current_pos < 0:
        current_pos += max_encoder_value
    if current_pos > max_encoder_value:
        current_pos -= max_encoder_value

    return current_pos

'''class Colors:
    IrSensors = 0xA32900
    BasePlate = 0x55AAEE
    Wheels = 0x000000'''
