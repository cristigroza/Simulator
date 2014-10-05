import sys
import threading
import socket
from server import Server
import sim_server_helpers

try:
    import Queue as queue
except ImportError:
    import queue

class SimServer:

    helpers = sim_server_helpers
    def __init__(self, robot,  tracker, log_queue, simParent):
        self._robot = robot

        self._tracker = tracker
        self._logqueue = log_queue
        self._out_server_queue = queue.Queue()
        self.init_server()
        self._simParent = simParent

    def init_server(self):
        self._server_thread = Server(self._out_server_queue, self._logqueue)
        self._in_server_queue = self._server_thread.getOutQueue()

    def set_robot(self, robot):
        self._robot = robot

    def set_server_log(self, show):
        self._server_thread.set_server_log(show)

    def process_queue(self):
        while not self._in_server_queue.empty():
            tpl = self.helpers.buildTuple(self._in_server_queue.get())

            if isinstance(tpl,tuple):
                name, args = tpl
                if name in self.__class__.__dict__:
                    try:
                        if args is None:
                            self.__class__.__dict__[name](self)
                        else:
                            self.__class__.__dict__[name](self,*args)
                    except TypeError as e:
                        self.log("Wrong sim_server event parameters {}{}".format(name,args))
                        raise e
                    except Exception as e:
                        self.log("EXCEPTION: {}".format(sys.exc_info()))
                        raise e

                else:
                    self.log("Unknown sim_server event '{}'".format(name))
            else:
                self.log("Wrong sim_server event format '{}'".format(tpl))


    def run(self, ipAddress, port):
        if not self._server_thread.run_server:
            self._server_thread._sock.close()
            self.init_server()

        if not self._server_thread.isAlive():
            self._server_thread.setIpAddress(ipAddress)
            self._server_thread.setPort(int(port))
            self._server_thread.start()
        else:
            self.log("Server is running...")


    def stop(self,ipAddress, port):
        self._server_thread.run_server = False
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.connect( (ipAddress, int(port)))
        temp_socket.close()

    time_constant = 0.02 # 20 milliseconds

    def DcMotorPositionTimeCtrAll(self, left_wheel, right_wheel, run_time):
        vl = self.helpers.computeWheelRotationSpeed(self._robot, left_wheel, self._robot.info.wheels.left_ticks, run_time)
        vr = self.helpers.computeWheelRotationSpeed(self._robot, right_wheel, self._robot.info.wheels.right_ticks, run_time)

        self._robot.info.wheels.left_ticks = left_wheel
        self._robot.info.wheels.right_ticks = right_wheel
        self.robot_move(vl,vr, run_time)
        self._out_server_queue.put("Done.")

    def DcMotorPwmTimeCtrAll(self, left_wheel_pwm_command, right_wheel_pwm_command, run_time):
        vl = self.helpers.convertPWMToVelocity(self._robot, left_wheel_pwm_command)
        vr = self.helpers.convertPWMToVelocity(self._robot, right_wheel_pwm_command)

        self._robot.info.wheels.left_ticks = self.helpers.convertVelocityToRobotTicks(vl, run_time, self._robot.info.wheels.left_ticks, self._robot.info)
        self._robot.info.wheels.right_ticks = self.helpers.convertVelocityToRobotTicks(vr, run_time, self._robot.info.wheels.right_ticks, self._robot.info)

        self.robot_move(vl,vr,run_time)
        self._out_server_queue.put("Done.")

    def robot_move(self,vl,vr,run_time):
        nrRuns = int(run_time/self.time_constant)

        for x in range(0, nrRuns):
            self._robot.set_inputs((vl,vr))
            self._robot.move(self.time_constant)

            self._tracker.add_point(self._robot.get_pose())
            self._simParent.check_collisions()
            self._simParent.draw()



    def get_ir_sensor_readings(self, ir_sensor_id):
        info = self._robot.get_info()
        return info.ir_sensors.readings[ir_sensor_id]

    def get_sonar_sensor_readings(self,sonar_sensor_id):
        info = self._robot.get_info()
        return info.sonar_sensors.readings[sonar_sensor_id]

    def getLeftWheelEncoderValue(self):
        self._out_server_queue.put(self._robot.info.wheels.left_ticks)

    def getRightWheelEncoderValue(self):
        self._out_server_queue.put(self._robot.info.wheels.right_ticks)
    #IR
    def GetIR1(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(0))

    def GetIR2(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(1))

    def GetIR3(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(2))

    def GetIR4(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(3))

    def GetIR5(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(4))

    def GetIR6(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(5))

    def GetIR7(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(6))

    def GetIR8(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(7))

    def GetIR9(self):
        self._out_server_queue.put(self.get_ir_sensor_readings(8))

    #Sonsr
    def GetSensorSonar1(self):
        self._out_server_queue.put(self.get_sonar_sensor_readings(0))

    def GetSensorSonar2(self):
        self._out_server_queue.put(self.get_sonar_sensor_readings(1))

    def GetSensorSonar3(self):
        self._out_server_queue.put(self.get_sonar_sensor_readings(2))

    def GetSensorSonar4(self):
        self._out_server_queue.put(self.get_sonar_sensor_readings(3))

    def GetSensorSonar5(self):
        self._out_server_queue.put(self.get_sonar_sensor_readings(4))

    def GetSensorSonar6(self):
        self._out_server_queue.put(self.get_sonar_sensor_readings(5))

    def log(self, message):
        print("{}: {}".format(self.__class__.__name__,message))
        if self._logqueue is not None:
            self._logqueue.append((self,message))